# src/Services/event_handlers/__init__.py
"""
Event Handlers Module
=====================
Manejadores de eventos para procesamiento de datos GPS y sensores.

Componentes:
- geofence_handler: Detección y logging de eventos de geocercas
- trip_handler: Detección y gestión del ciclo de vida de trips
- persistence_handler: Inserción de datos en DB con transacciones atómicas

Arquitectura:
- Handlers reciben inputs explícitos
- Retornan outputs sin side effects
- Error handling interno (no propagan excepciones)
- Testeables sin simular loops completos
"""

from .geofence_handler import handle_geofence_detection
from .trip_handler import (
    calculate_haversine_distance,
    calculate_trip_metrics,
    handle_trip_detection
)
from .persistence_handler import insert_data

__all__ = [
    # Geofence handler
    'handle_geofence_detection',
    
    # Trip handler
    'calculate_haversine_distance',
    'calculate_trip_metrics',
    'handle_trip_detection',
    
    # Persistence handler
    'insert_data',
]