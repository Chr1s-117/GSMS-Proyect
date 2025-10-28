# src/Services/geofence_detector.py

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text

# ✅ CORRECCIÓN 1: Import correcto
from src.Repositories.gps_data import get_last_gps_row_by_device
from src.Models.geofence import Geofence


class GeofenceDetector:
    """
    Servicio de detección de geocercas.
    Encapsula la lógica para determinar si un punto GPS se encuentra
    dentro o fuera de una geocerca activa.
    """

    def check_point(
        self,
        db: Session,
        device_id: str,
        lat: float,
        lon: float,
        timestamp: datetime
    ) -> Optional[Dict[str, Any]]:
        """
        Verifica si el punto GPS (lat, lon) se encuentra dentro de una geocerca.
        
        Returns:
            - Dict con 'id', 'name', 'event_type' si hay evento
            - None si no hay cambio (fuera sin cambios)
        """

        # Paso 1: buscar geocerca actual
        current_geofence = self._find_containing_geofence(db, lat, lon)

        # Paso 2: obtener último GPS del dispositivo
        previous_gps = get_last_gps_row_by_device(db, device_id)
        previous_geofence_id = (
            previous_gps.get('CurrentGeofenceID') if previous_gps else None
        )

        # Paso 3: matriz de decisión
        if current_geofence:
            current_id = current_geofence['id']

            if current_id != previous_geofence_id:
                # Cambio detectado: entrada o cambio de geocerca
                return {
                    'id': current_id,
                    'name': current_geofence['name'],
                    'event_type': 'entry'
                }
            else:
                # Sin cambio: sigue dentro
                return {
                    'id': current_id,
                    'name': current_geofence['name'],
                    'event_type': 'inside'
                }

        else:
            # No está en ninguna geocerca
            if previous_geofence_id:
                # Estaba en geocerca, ahora fuera → EXIT
                return {
                    'id': None,
                    'name': None,
                    'event_type': 'exit'
                }
            else:
                # Estaba fuera, sigue fuera
                return None

    def _find_containing_geofence(
        self,
        db: Session,
        lat: float,
        lon: float
    ) -> Optional[Dict[str, str]]:
        """
        Busca si el punto (lat, lon) está contenido dentro de alguna geocerca activa.
        Retorna la geocerca más específica (menor área).
        
        IMPORTANTE: PostGIS Geography NO soporta ST_Contains, usamos ST_Intersects
        """

        query = text("""
            SELECT id, name, ST_Area(geometry) AS area
            FROM geofences
            WHERE is_active = TRUE
            AND ST_Intersects(
                geometry,
                ST_GeogFromText('POINT(' || :lon || ' ' || :lat || ')')
            )
            ORDER BY area ASC
            LIMIT 1
        """)

        result = db.execute(query, {'lon': lon, 'lat': lat}).first()

        if result:
            return {
                'id': result.id if isinstance(result.id, str) else str(result.id),
                'name': result.name if isinstance(result.name, str) else str(result.name)
            }
        return None

    def _get_geofence_by_id(
        self, 
        db: Session, 
        geofence_id: str
    ) -> Optional[Dict[str, str]]:
        """
        Retorna información básica de una geocerca por ID.
        Usado opcionalmente para obtener info al salir (exit).
        """
        geofence = db.query(Geofence).filter(
            Geofence.id == geofence_id
        ).first()
        
        if geofence:
            return {
                'id': geofence.id if isinstance(geofence.id, str) else str(geofence.id),
                'name': geofence.name if isinstance(geofence.name, str) else str(geofence.name)
            }
        return None


# --------------------------------------------------------
# INSTANCIA GLOBAL (Singleton)
# --------------------------------------------------------
geofence_detector = GeofenceDetector()
