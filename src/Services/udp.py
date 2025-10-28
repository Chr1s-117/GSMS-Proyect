# src/Services/udp.py

"""
UDP Server for receiving GPS and Accelerometer data from devices.

✨ NEW FEATURES (v2):
- Dual data stream support: GPS + Accelerometer in single packet
- Robust timestamp normalization (handles seconds/milliseconds)
- Atomic transactions for dual inserts
- Non-blocking accel validation (GPS always inserted if valid)

- Normalizes incoming JSON payloads to match Pydantic schemas.
- Converts timestamps to UTC-aware datetime objects.
- Validates registered and active devices before insertion.
- Avoids duplicate entries using database constraints.
- Logs all received packets centrally using log_ws.
"""

import socket
import json
import threading
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

# GPS imports
from src.Schemas.gps_data import GpsData_create
from src.Repositories.gps_data import created_gps_data, get_last_gps_row_by_device

# Accelerometer imports
from src.Schemas.accelerometer_data import AccelData_create
from src.Repositories.accelerometer_data import create_accel_data

# Core imports
from src.Models.device import Device
from src.DB.session import SessionLocal
from src.Core import log_ws
from src.Services.geofence_detector import geofence_detector

# ==========================================================
# UDP CONFIGURATION
# ==========================================================
UDP_PORT = int(os.getenv("UDP_PORT", "9001"))
BUFFER_SIZE = 65535  # maximum safe UDP packet size

_ALLOWED_KEYS = {"DeviceID", "Latitude", "Longitude", "Altitude", "Accuracy", "Timestamp"}

_KEY_MAP = {
    # Device ID variants
    "device_id": "DeviceID",
    "deviceId": "DeviceID",
    "deviceid": "DeviceID",
    "device": "DeviceID",
    "DeviceID": "DeviceID",

    # GPS coordinate variants
    "latitude": "Latitude", "lat": "Latitude",
    "longitude": "Longitude", "lon": "Longitude", "lng": "Longitude",
    "altitude": "Altitude", "alt": "Altitude",
    "accuracy": "Accuracy", "acc": "Accuracy",

    # Timestamp variants
    "timestamp": "Timestamp", "time": "Timestamp",
    "timeStamp": "Timestamp",
}

# ==========================================================
# TIMESTAMP NORMALIZATION
# ==========================================================

def _normalize_timestamp(ts_value: Any) -> datetime:
    """
    Normaliza timestamp a datetime UTC-aware.
    
    Soporta múltiples formatos:
    - datetime objects (con o sin timezone)
    - UNIX timestamp en segundos (1730000000)
    - UNIX timestamp en milisegundos (1730000000000)
    - Strings numéricos de cualquiera de los anteriores
    
    Args:
        ts_value: Timestamp en cualquier formato soportado
        
    Returns:
        datetime: UTC-aware datetime object
        
    Raises:
        ValueError: Si el formato no es reconocible
        
    Examples:
        >>> _normalize_timestamp(1730000000)
        datetime(2024, 10, 27, 4, 0, tzinfo=timezone.utc)
        
        >>> _normalize_timestamp(1730000000000)
        datetime(2024, 10, 27, 4, 0, tzinfo=timezone.utc)
        
        >>> _normalize_timestamp("1730000000.123")
        datetime(2024, 10, 27, 4, 0, 0, 123000, tzinfo=timezone.utc)
    """
    # Ya es datetime
    if isinstance(ts_value, datetime):
        return ts_value if ts_value.tzinfo else ts_value.replace(tzinfo=timezone.utc)
    
    # Convertir a float
    try:
        ts_float = float(ts_value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid timestamp format: {ts_value}") from e
    
    # Heurística: timestamps > 10^10 son milisegundos
    # Año 2286 en segundos = 10^10
    # Año 2001 en milisegundos = 10^12
    if ts_float > 10_000_000_000:
        ts_float = ts_float / 1000.0
    
    return datetime.fromtimestamp(ts_float, tz=timezone.utc)


# ==========================================================
# JSON EXTRACTION & NORMALIZATION
# ==========================================================

def _extract_json_candidate(s: str) -> str:
    """Extrae el objeto JSON más externo de un string."""
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1 and end > start:
        return s[start:end+1]
    return s


def _coerce_number(value: Any):
    """Convierte strings numéricos a float, maneja null/empty."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        v = value.strip()
        if v == "" or v.lower() == "null":
            return None
        v = v.replace(",", ".")
        try:
            return float(v)
        except:
            return value
    return value


def _normalize_payload(raw_payload: Any) -> Dict[str, Any]:
    """
    Normaliza payload GPS del formato UDP al schema interno.
    
    - Mapea claves alternativas (deviceId → DeviceID)
    - Filtra campos no permitidos
    - Convierte números en strings a float
    """
    if isinstance(raw_payload, dict) and len(raw_payload) == 1:
        only_key = next(iter(raw_payload))
        candidate = raw_payload[only_key] if isinstance(raw_payload[only_key], dict) else raw_payload
    else:
        candidate = raw_payload if isinstance(raw_payload, dict) else {}

    normalized: Dict[str, Any] = {}
    for k, v in candidate.items():
        mapped = _KEY_MAP.get(k, _KEY_MAP.get(k.lower(), k))
        if mapped in _ALLOWED_KEYS:
            normalized[mapped] = _coerce_number(v)
    return normalized


# ==========================================================
# ACCELEROMETER DATA EXTRACTION
# ==========================================================

def _extract_accel_data(
    raw_payload: dict, 
    device_id: str, 
    gps_timestamp: datetime
) -> Optional[Dict[str, Any]]:
    """
    Extrae datos de acelerómetro del payload UDP y los normaliza
    para el schema AccelData_create.
    
    Estructura esperada en raw_payload:
```json
    {
      "accel": {
        "ts_start": 1730000000000,
        "ts_end": 1730000001000,
        "rms": {"x": 0.5, "y": 0.6, "z": 0.4, "mag": 0.9},
        "max": {"x": 1.2, "y": 1.5, "z": 1.0, "mag": 2.1},
        "peaks_count": 3,
        "sample_count": 250,
        "flags": 0
      }
    }
```
    
    Args:
        raw_payload: JSON crudo recibido por UDP
        device_id: ID del dispositivo (ya validado)
        gps_timestamp: Timestamp GPS (ya normalizado a datetime UTC)
    
    Returns:
        Dict listo para AccelData_create o None si:
        - No hay campo 'accel' en el payload
        - Los datos de accel son inválidos/incompletos
        
    Raises:
        No levanta excepciones (retorna None en caso de error)
    """
    accel = raw_payload.get('accel')
    if not accel:
        return None
    
    try:
        # Timestamps de la ventana (UNIX ms → datetime UTC)
        ts_start = _normalize_timestamp(accel['ts_start'])
        ts_end = _normalize_timestamp(accel['ts_end'])
        
        # Aplanar estructura anidada
        rms = accel.get('rms', {})
        max_vals = accel.get('max', {})
        
        return {
            'DeviceID': device_id,
            'Timestamp': gps_timestamp,  # ← Mismo que GPS para correlación
            'ts_start': ts_start,
            'ts_end': ts_end,
            'rms_x': float(rms.get('x', 0.0)),
            'rms_y': float(rms.get('y', 0.0)),
            'rms_z': float(rms.get('z', 0.0)),
            'rms_mag': float(rms.get('mag', 0.0)),
            'max_x': float(max_vals.get('x', 0.0)),
            'max_y': float(max_vals.get('y', 0.0)),
            'max_z': float(max_vals.get('z', 0.0)),
            'max_mag': float(max_vals.get('mag', 0.0)),
            'peaks_count': int(accel.get('peaks_count', 0)),
            'sample_count': int(accel.get('sample_count', 250)),
            'flags': int(accel.get('flags', 0))
        }
    
    except (KeyError, ValueError, TypeError) as e:
        print(f"[UDP] Error extracting accel data: {e}")
        return None


# ==========================================================
# UDP SERVER MAIN LOGIC
# ==========================================================

def udp_server():
    """
    Main UDP server loop.
    
    Flow:
    1. Receive UDP packet
    2. Parse JSON (with fallbacks for malformed data)
    3. Normalize GPS payload
    4. Extract accelerometer payload (if present)
    5. Validate device (registered + active)
    6. Validate GPS schema (required)
    7. Validate Accel schema (optional, non-blocking)
    8. Detect geofence events
    9. Insert to database (atomic transaction)
    10. Update device LastSeen
    """
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("0.0.0.0", UDP_PORT))
    print(f"[UDP] Server listening on port {UDP_PORT}")

    while True:
        try:
            data, addr = udp_sock.recvfrom(BUFFER_SIZE)
            sender_ip, sender_port = addr[0], addr[1]
            print(f"[UDP] Received {len(data)} bytes from {sender_ip}:{sender_port}")

            # ========================================
            # PASO 1: DECODE UTF-8
            # ========================================
            try:
                json_str = data.decode("utf-8").strip()
            except UnicodeDecodeError:
                json_str = data.decode("utf-8", errors="replace").strip()
                print(f"[UDP] Warning: decode replaced invalid bytes from {sender_ip}:{sender_port}")

            json_str = json_str.lstrip("\ufeff").strip()  # Remove BOM

            # ========================================
            # PASO 2: PARSE JSON (con fallbacks)
            # ========================================
            try:
                raw_payload = json.loads(json_str)
            except json.JSONDecodeError:
                # Intento 1: Extraer JSON válido del string
                candidate = _extract_json_candidate(json_str)
                try:
                    raw_payload = json.loads(candidate)
                except json.JSONDecodeError:
                    # Intento 2: Reemplazar comillas simples
                    try:
                        raw_payload = json.loads(json_str.replace("'", '"'))
                    except json.JSONDecodeError as jde2:
                        print(f"[UDP] JSON decode error from {sender_ip}:{sender_port}: {jde2}")
                        continue

            # ========================================
            # PASO 3: NORMALIZAR PAYLOAD GPS
            # ========================================
            normalized = _normalize_payload(raw_payload)

            # Normalizar timestamp GPS
            ts_value = normalized.get("Timestamp")
            if ts_value is not None:
                try:
                    normalized["Timestamp"] = _normalize_timestamp(ts_value)
                except ValueError as e:
                    print(f"[UDP] Invalid timestamp {ts_value} from {sender_ip}:{sender_port}: {e}")
                    continue

            if not normalized:
                print(f"[UDP] Normalized payload empty from {sender_ip}:{sender_port} - skipping")
                continue

            # ========================================
            # PASO 4: VALIDAR SCHEMA GPS (REQUERIDO)
            # ========================================
            try:
                gps_data = GpsData_create(**normalized)
            except ValidationError as ve:
                print(f"[UDP] GPS ValidationError from {sender_ip}:{sender_port}: {ve} | normalized: {normalized}")
                continue

            # ========================================
            # PASO 5: VALIDAR DEVICE ID
            # ========================================
            device_id = normalized.get("DeviceID")
            if not device_id:
                print(f"[UDP] Missing DeviceID from {sender_ip}:{sender_port} - REJECTED")
                log_ws.log_from_thread(
                    f"[UDP] SECURITY: Rejected packet without DeviceID from {sender_ip}:{sender_port}",
                    msg_type="error"
                )
                continue

            # ========================================
            # PASO 6: EXTRAER Y VALIDAR ACCEL (OPCIONAL)
            # ========================================
            accel_data = None
            if 'accel' in raw_payload:
                try:
                    accel_dict = _extract_accel_data(raw_payload, device_id, gps_data.Timestamp)
                    if accel_dict:
                        accel_data = AccelData_create(**accel_dict)
                        print(f"[UDP] Accel data validated for {device_id}")
                except ValidationError as ve:
                    # ⚠️ Accel inválido NO rechaza el paquete completo
                    log_ws.log_from_thread(
                        f"[UDP] Accel validation error for {device_id}, GPS will still be inserted: {ve}",
                        msg_type="warning"
                    )
                    print(f"[UDP] Accel validation failed: {ve}")

            # ========================================
            # PASO 7: VALIDAR DEVICE EN DB
            # ========================================
            try:
                with SessionLocal() as db:
                    # Verificar device registrado y activo
                    device_record = db.query(Device).filter(Device.DeviceID == device_id).first()

                    if not device_record:
                        print(f"[UDP] Unregistered device '{device_id}' from {sender_ip}:{sender_port} - REJECTED")
                        log_ws.log_from_thread(
                            f"[UDP] SECURITY: Rejected data from unregistered device '{device_id}' (IP: {sender_ip}:{sender_port})",
                            msg_type="error"
                        )
                        continue

                    if device_record.IsActive is False:
                        print(f"[UDP] Inactive device '{device_id}' from {sender_ip}:{sender_port} - REJECTED")
                        log_ws.log_from_thread(
                            f"[UDP] SECURITY: Rejected data from inactive device '{device_id}' (IP: {sender_ip}:{sender_port})",
                            msg_type="error"
                        )
                        continue

                    # ✅ Device válido: proceder con inserción
                    try:
                        incoming_dict = gps_data.model_dump()
                        log_ws.log_from_thread(
                            f"[UDP] Device '{device_id}' from {sender_ip}: GPS={incoming_dict}, Accel={'present' if accel_data else 'none'}",
                            msg_type="log"
                        )

                        # ========================================
                        # PASO 8: DETECCIÓN DE GEOCERCA
                        # ========================================
                        try:
                            # Obtener GPS anterior
                            previous_gps = get_last_gps_row_by_device(db, device_id)
                            
                            # Detectar geocerca
                            geofence_info = geofence_detector.check_point(
                                db=db,
                                device_id=device_id,
                                lat=gps_data.Latitude,
                                lon=gps_data.Longitude,
                                timestamp=gps_data.Timestamp
                            )
                            
                            if geofence_info:
                                # Si es ENTRY y había geocerca anterior, crear EXIT artificial
                                if (
                                    geofence_info['event_type'] == 'entry' and 
                                    previous_gps and 
                                    previous_gps.get('CurrentGeofenceID')
                                ):
                                    # Crear registro EXIT artificial 1 μs antes
                                    exit_dict = {
                                        'DeviceID': device_id,
                                        'Latitude': gps_data.Latitude,
                                        'Longitude': gps_data.Longitude,
                                        'Altitude': gps_data.Altitude,
                                        'Accuracy': gps_data.Accuracy,
                                        'Timestamp': gps_data.Timestamp - timedelta(microseconds=1),
                                        'CurrentGeofenceID': previous_gps['CurrentGeofenceID'],
                                        'CurrentGeofenceName': previous_gps['CurrentGeofenceName'],
                                        'GeofenceEventType': 'exit'
                                    }
                                    created_gps_data(db, GpsData_create(**exit_dict))
                                    log_ws.log_from_thread(
                                        f"[GEOFENCE] {device_id} EXITED {previous_gps['CurrentGeofenceName']}",
                                        msg_type="log"
                                    )

                                # Continuar con flujo normal
                                incoming_dict['CurrentGeofenceID'] = geofence_info['id']
                                incoming_dict['CurrentGeofenceName'] = geofence_info['name']
                                incoming_dict['GeofenceEventType'] = geofence_info['event_type']

                                # LOG solo ENTRY/EXIT
                                if geofence_info['event_type'] in ('entry', 'exit'):
                                    action = "ENTERED" if geofence_info['event_type'] == 'entry' else "EXITED"
                                    
                                    # Para EXIT, usar nombre de geocerca anterior
                                    if geofence_info['event_type'] == 'exit':
                                        geo_name = previous_gps.get('CurrentGeofenceName', 'Unknown Zone') if previous_gps else 'Unknown Zone'
                                    else:
                                        geo_name = geofence_info.get('name', 'Unknown')
                                    
                                    log_ws.log_from_thread(
                                        f"[GEOFENCE] {device_id} {action} {geo_name}",
                                        msg_type="log"
                                    )

                            else:
                                incoming_dict['CurrentGeofenceID'] = None
                                incoming_dict['CurrentGeofenceName'] = None
                                incoming_dict['GeofenceEventType'] = None
                                
                        except Exception as geo_error:
                            print(f"[UDP] Geofence detection error for {device_id}: {geo_error}")
                            incoming_dict['CurrentGeofenceID'] = None
                            incoming_dict['CurrentGeofenceName'] = None
                            incoming_dict['GeofenceEventType'] = None

                        # ========================================
                        # PASO 9: INSERCIÓN EN DB (TRANSACCIÓN ATÓMICA)
                        # ========================================
                        
                        # 1️⃣ Insertar accel primero (si existe y es válido)
                        accel_inserted = False
                        if accel_data:
                            try:
                                create_accel_data(db, accel_data)
                                accel_inserted = True
                                log_ws.log_from_thread(
                                    f"[UDP] Device '{device_id}': Accel data inserted",
                                    msg_type="log"
                                )
                            except IntegrityError as ie:
                                # Accel duplicado (constraint unique_device_timestamp_accel)
                                error_str = str(ie).lower()
                                if "unique_device_timestamp" in error_str or "duplicate key" in error_str:
                                    print(f"[UDP] Device '{device_id}': Duplicate accel (DeviceID+Timestamp) - skipped")
                                    db.rollback()
                                    # Continuar para insertar GPS
                                else:
                                    # Error no esperado en accel
                                    print(f"[UDP] Device '{device_id}': Unexpected accel DB error: {ie}")
                                    db.rollback()
                                    # Continuar para insertar GPS
                        
                        # 2️⃣ Insertar GPS (siempre)
                        new_row = created_gps_data(db, GpsData_create(**incoming_dict))
                        
                        # 3️⃣ Update LastSeen
                        setattr(device_record, "LastSeen", gps_data.Timestamp)
                        db.commit()
                        
                        # Log resultado
                        insert_summary = f"GPS (ID: {new_row.id})"
                        if accel_inserted:
                            insert_summary += " + Accel"
                        
                        log_ws.log_from_thread(
                            f"[UDP] Device '{device_id}': {insert_summary} inserted successfully",
                            msg_type="log"
                        )

                    except IntegrityError as ie:
                        db.rollback()
                        error_str = str(ie).lower()
                        
                        if "unique_device_timestamp" in error_str or "duplicate key" in error_str:
                            print(f"[UDP] Device '{device_id}': Duplicate GPS (DeviceID+Timestamp) - skipped")
                        else:
                            print(f"[UDP] Device '{device_id}': Unexpected GPS DB error: {ie}")
                            log_ws.log_from_thread(
                                f"[UDP] GPS DB error for device '{device_id}': {ie}",
                                msg_type="error"
                            )

            except Exception as outer_error:
                print(f"[UDP] Critical error processing packet from {sender_ip}:{sender_port}: {outer_error}")
                log_ws.log_from_thread(
                    f"[UDP] Critical error from {sender_ip}:{sender_port}: {outer_error}",
                    msg_type="error"
                )

        except Exception as e:
            print(f"[UDP] Error receiving/processing data: {e}")


def start_udp_server() -> threading.Thread:
    """
    Inicia el servidor UDP en un thread daemon.
    
    Returns:
        threading.Thread: Thread del servidor (ya iniciado)
    """
    thread = threading.Thread(target=udp_server, daemon=True, name="UDP-Server")
    thread.start()
    print("[UDP] Background thread started")
    return thread