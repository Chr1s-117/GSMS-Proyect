# src/Services/udp_core/__init__.py
"""
UDP Core Module
===============
Módulo encapsulado para manejo de paquetes UDP.

Componentes:
- packet_parser: Parsing de paquetes UDP con fallbacks robustos
- normalizers: Normalización de payloads GPS a schema interno
- data_extractors: Extracción de datos específicos por tipo de sensor
- validators: Validación de dispositivos y schemas de datos
"""

from .packet_parser import parse_udp_packet, _extract_json_candidate
from .normalizers import (
    ALLOWED_KEYS,
    KEY_MAP,
    coerce_number,
    normalize_timestamp,
    normalize_gps_payload
)
from .data_extractors import (
    extract_accel_data,
    extract_obd_data,
    extract_temp_data
)
from .validators import (
    validate_device,
    validate_gps_schema,
    validate_accel_schema,
    validate_obd_schema,
    validate_device_permissions
)

__all__ = [
    # Packet parser
    'parse_udp_packet',
    '_extract_json_candidate',
    
    # Normalizers - Constants
    'ALLOWED_KEYS',
    'KEY_MAP',
    
    # Normalizers - Functions
    'coerce_number',
    'normalize_timestamp',
    'normalize_gps_payload',
    
    # Data extractors
    'extract_accel_data',
    'extract_obd_data',
    'extract_temp_data',
    
    # Validators
    'validate_device',
    'validate_gps_schema',
    'validate_accel_schema',
    'validate_obd_schema',
    'validate_device_permissions',
]