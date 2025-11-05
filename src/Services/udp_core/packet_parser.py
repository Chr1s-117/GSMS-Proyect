# src/Services/udp_core/packet_parser.py
"""
UDP Packet Parser Module
=========================
Encapsula toda la lógica de parsing de paquetes UDP con múltiples fallbacks.

Extraído de udp.py (Fase 2) para:
- Reutilización en otros protocolos (TCP, HTTP)
- Testing unitario con payloads malformados
- Mantenibilidad centralizada del formato JSON

Fallbacks implementados:
1. Decode UTF-8 normal
2. Decode UTF-8 con replace de bytes inválidos
3. Extracción de objeto JSON más externo
4. Reemplazo de comillas simples por dobles
"""

import json
from typing import Dict, Any


def _extract_json_candidate(s: str) -> str:
    """
    Extrae el objeto JSON más externo de un string.
    
    Útil cuando el payload contiene basura antes/después del JSON válido.
    
    Args:
        s: String que potencialmente contiene JSON
        
    Returns:
        str: Substring desde el primer '{' hasta el último '}'
        
    Examples:
        >>> _extract_json_candidate('garbage{"key":"value"}more garbage')
        '{"key":"value"}'
        >>> _extract_json_candidate('no json here')
        'no json here'
    """
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1 and end > start:
        return s[start:end+1]
    return s


def parse_udp_packet(data: bytes, sender_ip: str, sender_port: int) -> Dict[str, Any]:
    """
    Parse UDP packet con múltiples fallbacks para manejar datos malformados.
    
    Estrategia de fallbacks:
    1. UTF-8 decode normal + JSON parse directo
    2. UTF-8 decode con replace + JSON parse directo
    3. Extracción de objeto JSON más externo + parse
    4. Reemplazo de comillas simples por dobles + parse
    
    Args:
        data: Raw bytes del paquete UDP
        sender_ip: IP del remitente (para logging)
        sender_port: Puerto del remitente (para logging)
        
    Returns:
        dict: Payload JSON parseado
        
    Raises:
        ValueError: Si ningún fallback logra parsear el JSON
        
    Examples:
        >>> data = b'{"DeviceID": "test123", "Latitude": 10.5}'
        >>> parse_udp_packet(data, "192.168.1.1", 5000)
        {'DeviceID': 'test123', 'Latitude': 10.5}
        
    Notes:
        - Elimina BOM (Byte Order Mark) si está presente
        - Los fallbacks son progresivamente más permisivos
        - Logs warnings cuando usa fallbacks
    """
    # ========================================
    # FALLBACK 1: DECODE UTF-8 NORMAL
    # ========================================
    try:
        json_str = data.decode("utf-8").strip()
    except UnicodeDecodeError:
        # FALLBACK 2: DECODE CON REPLACE
        json_str = data.decode("utf-8", errors="replace").strip()
        print(f"[PARSER] Warning: decode replaced invalid bytes from {sender_ip}:{sender_port}")
    
    # Eliminar BOM (Byte Order Mark) si existe
    json_str = json_str.lstrip("\ufeff").strip()
    
    # ========================================
    # FALLBACK 1: JSON PARSE DIRECTO
    # ========================================
    try:
        raw_payload = json.loads(json_str)
        return raw_payload
    except json.JSONDecodeError:
        pass  # Intentar fallback 2
    
    # ========================================
    # FALLBACK 2: EXTRAER OBJETO JSON MÁS EXTERNO
    # ========================================
    candidate = _extract_json_candidate(json_str)
    try:
        raw_payload = json.loads(candidate)
        print(f"[PARSER] Warning: used JSON extraction fallback for {sender_ip}:{sender_port}")
        return raw_payload
    except json.JSONDecodeError:
        pass  # Intentar fallback 3
    
    # ========================================
    # FALLBACK 3: REEMPLAZAR COMILLAS SIMPLES
    # ========================================
    try:
        raw_payload = json.loads(json_str.replace("'", '"'))
        print(f"[PARSER] Warning: used quote replacement fallback for {sender_ip}:{sender_port}")
        return raw_payload
    except json.JSONDecodeError as jde:
        # Todos los fallbacks fallaron
        raise ValueError(
            f"JSON decode failed after all fallbacks from {sender_ip}:{sender_port}: {jde}"
        ) from jde