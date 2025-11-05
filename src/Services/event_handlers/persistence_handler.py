# src/Services/event_handlers/persistence_handler.py
"""
Persistence Handler
===================
Maneja la inserción de datos GPS y Acelerómetro en la base de datos.

Extraído de udp.py (Fase 8) para:
- Separar lógica de persistencia de lógica de negocio
- Manejar transacciones atómicas (accel + GPS)
- Facilitar testing de inserción sin simular todo el loop UDP
- Centralizar manejo de duplicados y errores de DB

Arquitectura:
- Input: Datos validados (GPS, Accel, Device, trip_id)
- Output: Tupla (gps_inserted, accel_inserted)
- Transacción atómica: Accel → GPS → update LastSeen → commit
- Non-blocking accel: Si accel falla, GPS continúa

Funciones:
- insert_data(): Inserta GPS + Accel en una transacción atómica
"""

from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Imports de repositories
from src.Repositories.gps_data import created_gps_data
from src.Repositories.accelerometer_data import create_accel_data
from src.Repositories.trip import increment_point_count

# Imports de schemas
from src.Schemas.gps_data import GpsData_create
from src.Schemas.accelerometer_data import AccelData_create

# Imports de modelos
from src.Models.device import Device

# Imports de logging
from src.Core import log_ws
from datetime import datetime

def insert_data(
    db: Session,
    gps_data: GpsData_create,
    accel_data: Optional[AccelData_create],
    device_record: Device,
    trip_id: Optional[str] = None
) -> Tuple[bool, bool]:
    """
    Inserta GPS y Acelerómetro en la DB con transacción atómica.
    
    Orden de operaciones:
    1. Insertar Accel (non-blocking si falla)
    2. Insertar GPS (siempre, crítico)
    3. Incrementar point_count del trip (si aplica)
    4. Actualizar LastSeen del device
    5. Commit de la transacción
    6. Log del resultado
    
    Filosofía de errores:
    - Accel es "nice to have" → si falla, continúa con GPS
    - GPS es crítico → si falla, rollback completo
    - Duplicados son silenciosos (no son errores reales)
    
    ⚠️ IMPORTANTE: Orden de Inserción
    Accel se inserta PRIMERO para que:
    - Si accel falla (duplicate), GPS aún se puede insertar
    - Si GPS falla (duplicate), no queremos accel huérfano
    - Rollback parcial solo afecta al accel, no al GPS
    
    Args:
        db: Sesión de SQLAlchemy activa
        gps_data: Datos GPS validados (GpsData_create)
        accel_data: Datos Accel validados (opcional)
        device_record: Objeto Device de SQLAlchemy (para update LastSeen)
        trip_id: ID del trip activo (opcional, para asociar GPS)
        
    Returns:
        tuple[bool, bool]: (gps_inserted, accel_inserted)
            - (True, True): Ambos insertados exitosamente
            - (True, False): Solo GPS insertado (accel duplicado o falló)
            - (False, False): Nada insertado (GPS duplicado)
            - (False, True): Imposible (accel se rollback si GPS falla)
            
    Examples:
        >>> # Insertar GPS + Accel
        >>> gps_inserted, accel_inserted = insert_data(
        ...     db=db,
        ...     gps_data=gps_data,
        ...     accel_data=accel_data,
        ...     device_record=device,
        ...     trip_id="TRIP_20241027_120530_ESP32_001"
        ... )
        >>> if gps_inserted:
        ...     print("GPS guardado exitosamente")
        >>> if accel_inserted:
        ...     print("Accel guardado exitosamente")
        
        >>> # Insertar solo GPS (sin accel)
        >>> gps_inserted, _ = insert_data(
        ...     db=db,
        ...     gps_data=gps_data,
        ...     accel_data=None,
        ...     device_record=device,
        ...     trip_id=None
        ... )
        
    Side Effects:
        - Inserta registros en tabla gps_data
        - Inserta registros en tabla accelerometer_data (si accel_data)
        - Incrementa point_count en tabla trips (si trip_id)
        - Actualiza LastSeen en tabla devices
        - Escribe logs via log_ws.log_from_thread()
        
    Notes:
        - El commit() se hace al final, después de todas las operaciones
        - Si GPS falla, se hace rollback() completo (incluye accel si se insertó)
        - Duplicados GPS/Accel son silenciosos (no logueados como errores)
        - trip_id se agrega DESPUÉS de validación Pydantic (no está en schema)
    """
    device_id = gps_data.DeviceID
    
    # ========================================
    # PASO 1: INSERTAR ACELERÓMETRO (NON-BLOCKING)
    # ========================================
    accel_inserted = False
    
    if accel_data:
        try:
            create_accel_data(db, accel_data)
            accel_inserted = True
            print(f"[PERSISTENCE] Device '{device_id}': Accel data inserted")
            
        except IntegrityError as ie:
            # Error de integridad en accel (probablemente duplicado)
            error_str = str(ie).lower()
            
            if "unique_device_timestamp" in error_str or "duplicate key" in error_str:
                # Duplicado esperado (device envió mismo paquete 2 veces)
                print(f"[PERSISTENCE] Device '{device_id}': Duplicate accel (DeviceID+Timestamp) - skipped")
                db.rollback()  # ← Rollback SOLO del accel, GPS continúa
                
            else:
                # Error inesperado de DB
                print(f"[PERSISTENCE] Device '{device_id}': Unexpected accel DB error: {ie}")
                db.rollback()
                # GPS continúa de todos modos (accel es opcional)
    
    # ========================================
    # PASO 2: INSERTAR GPS (CRÍTICO)
    # ========================================
    
    # Agregar trip_id al GPS (después de validación Pydantic)
    gps_dict = gps_data.model_dump()
    gps_dict['trip_id'] = trip_id
    
    try:
        # Insertar GPS en DB
        new_row = created_gps_data(db, GpsData_create(**gps_dict))
        
        # ========================================
        # PASO 2.5: INCREMENTAR POINT_COUNT DEL TRIP
        # ========================================
        if trip_id:
            try:
                increment_point_count(db, trip_id)
            except Exception as trip_error:
                # Error incrementando point_count - no crítico
                print(f"[PERSISTENCE] Device '{device_id}': Error incrementing point_count: {trip_error}")
                # Continúa con commit del GPS (point_count no es crítico)
        
        # ========================================
        # PASO 3: ACTUALIZAR LASTSEEN DEL DEVICE
        # ========================================
        setattr(device_record, "LastSeen", gps_data.Timestamp)
        
        # ========================================
        # PASO 4: COMMIT DE LA TRANSACCIÓN
        # ========================================
        db.commit()
        
        # ========================================
        # PASO 5: LOG DEL RESULTADO
        # ========================================
        insert_summary = f"GPS (ID: {new_row.id})"
        if accel_inserted:
            insert_summary += " + Accel"
        
        log_ws.log_from_thread(
            f"[PERSISTENCE] Device '{device_id}': {insert_summary} inserted successfully",
            msg_type="log"
        )
        
        return True, accel_inserted
    
    except IntegrityError as ie:
        # Error de integridad en GPS
        db.rollback()  # ← Rollback completo (GPS + accel si se insertó)
        error_str = str(ie).lower()
        
        if "unique_device_timestamp" in error_str or "duplicate key" in error_str:
            # Duplicado GPS esperado (device envió mismo paquete 2 veces)
            print(f"[PERSISTENCE] Device '{device_id}': Duplicate GPS (DeviceID+Timestamp) - skipped")
            # No loguear como error (es comportamiento esperado)
            
        else:
            # Error inesperado de GPS DB
            print(f"[PERSISTENCE] Device '{device_id}': Unexpected GPS DB error: {ie}")
            log_ws.log_from_thread(
                f"[PERSISTENCE] GPS DB error for device '{device_id}': {ie}",
                msg_type="error"
            )
        
        return False, False  # ← Nada se insertó (rollback completo)
    
    except Exception as unexpected_error:
        # Error inesperado durante commit
        db.rollback()
        print(f"[PERSISTENCE] Device '{device_id}': Unexpected error during commit: {unexpected_error}")
        log_ws.log_from_thread(
            f"[PERSISTENCE] Unexpected error for device '{device_id}': {unexpected_error}",
            msg_type="error"
        )
        
        return False, False


# ==========================================================
# HELPER: BATCH INSERT (FUTURO)
# ==========================================================

def insert_data_batch(
    db: Session,
    gps_batch: list[GpsData_create],
    accel_batch: list[AccelData_create],
    device_id: str
) -> Tuple[int, int]:
    """
    [FUTURO] Inserta múltiples GPS + Accel en una sola transacción.
    
    Útil para:
    - Recuperación de datos offline (device estuvo sin conexión)
    - Importación de datos históricos
    - Batch processing de archivos
    
    Args:
        db: Sesión de SQLAlchemy
        gps_batch: Lista de GPS a insertar
        accel_batch: Lista de Accel a insertar
        device_id: ID del dispositivo
        
    Returns:
        tuple[int, int]: (gps_count, accel_count) insertados
    """
    # TODO: Implementar cuando se requiera batch processing
    raise NotImplementedError("Batch insert not yet implemented")


def update_device_last_seen_bulk(
    db: Session,
    device_updates: dict[str, datetime]
) -> int:
    """
    [FUTURO] Actualiza LastSeen de múltiples devices en una sola query.
    
    Útil para:
    - Batch processing
    - Sincronización periódica
    - Optimización de performance
    
    Args:
        db: Sesión de SQLAlchemy
        device_updates: {device_id: last_seen_timestamp}
        
    Returns:
        int: Número de devices actualizados
    """
    # TODO: Implementar cuando se requiera bulk updates
    raise NotImplementedError("Bulk update not yet implemented")