# src/Services/udp.py

"""
UDP Server Service for GPS Data Reception

This module implements a high-performance UDP server designed to handle
real-time GPS packets sent by devices. It ensures data integrity, 
normalization, validation, deduplication, geofence detection, and centralized logging.

Key features:
- Multi-device support with DeviceID validation
- Device registration and activation status checks (security layer)
- Normalizes incoming JSON payloads to match Pydantic schemas
- Converts incoming timestamps to UTC-aware datetime objects (ISO 8601 compatible)
- Prevents duplicate inserts using unique constraint (DeviceID, Timestamp)
- Real-time geofence detection with entry/exit event generation
- Automatic EXIT event creation when entering new geofence from another
- Updates device LastSeen timestamp on successful GPS insertion
- Logs all received packets centrally through log_ws
- Runs in a daemon thread to operate asynchronously alongside FastAPI

Architecture:
1. JSON normalization (handle malformed/alternative formats)
2. Pydantic validation (GpsData_create schema)
3. Device validation (registered, active)
4. Geofence detection (entry/exit/inside events)
5. Database insertion with duplicate prevention
6. Device LastSeen update
7. WebSocket broadcasting (via log_ws)
"""

import socket
import json
import threading
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from pydantic import ValidationError
from src.Schemas.gps_data import GpsData_create
from src.Repositories.gps_data import created_gps_data, get_last_gps_row_by_device
from src.Models.device import Device
from src.DB.session import SessionLocal
from src.Core import log_ws
from src.Services.geofence_detector import geofence_detector

# ==========================================================
# UDP Server Configuration
# ==========================================================
UDP_PORT = int(os.getenv("UDP_PORT", "9001"))  # Use environment variable if set
BUFFER_SIZE = 65535  # Maximum safe UDP packet size

# ==========================================================
# Field Normalization Configuration
# ==========================================================
_ALLOWED_KEYS = {
    "DeviceID", "Latitude", "Longitude", "Altitude", "Accuracy", "Timestamp"
}

_KEY_MAP = {
    # Device ID variants (case-insensitive)
    "device_id": "DeviceID",
    "deviceId": "DeviceID",
    "deviceid": "DeviceID",
    "device": "DeviceID",
    "DeviceID": "DeviceID",
    "DEVICE_ID": "DeviceID",

    # GPS coordinate variants
    "latitude": "Latitude", "lat": "Latitude", "Latitude": "Latitude",
    "longitude": "Longitude", "lon": "Longitude", "lng": "Longitude", "Longitude": "Longitude",
    "altitude": "Altitude", "alt": "Altitude", "Altitude": "Altitude",
    "accuracy": "Accuracy", "acc": "Accuracy", "Accuracy": "Accuracy",

    # Timestamp variants
    "timestamp": "Timestamp", "time": "Timestamp",
    "timeStamp": "Timestamp", "Timestamp": "Timestamp",
}


# ==========================================================
# JSON Normalization Helpers
# ==========================================================

def _extract_json_candidate(s: str) -> str:
    """
    Extract JSON object from string by finding outermost braces.
    
    Handles cases where JSON is embedded in additional text.
    
    Args:
        s: String potentially containing JSON
        
    Returns:
        Extracted JSON string or original string if no braces found
        
    Example:
        "some text {\"lat\": 10.5} more text" -> "{\"lat\": 10.5}"
    """
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1 and end > start:
        return s[start:end+1]
    return s


def _coerce_number(value: Any) -> Optional[float]:
    """
    Coerce various number formats to float.
    
    Handles:
    - Strings with commas as decimal separators ("10,5" -> 10.5)
    - Empty strings or "null" -> None
    - Already numeric values (passthrough)
    
    Args:
        value: Value to coerce
        
    Returns:
        Float value or None if coercion fails
        
    Example:
        _coerce_number("10,5") -> 10.5
        _coerce_number("") -> None
        _coerce_number(10.5) -> 10.5
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        v = value.strip()
        if v == "" or v.lower() == "null":
            return None
        v = v.replace(",", ".")  # Handle European decimal format
        try:
            return float(v)
        except:
            return value
    return value


def _normalize_payload(raw_payload: Any) -> Dict[str, Any]:
    """
    Normalize incoming JSON payload to standard GPS data structure.
    
    Handles:
    - Nested single-key objects (unwrapping)
    - Alternative field names (via _KEY_MAP)
    - Number format coercion
    - Field filtering (only _ALLOWED_KEYS)
    
    Args:
        raw_payload: Raw JSON data from UDP packet
        
    Returns:
        Normalized dictionary with standardized field names
        
    Example:
        Input: {"gps": {"lat": "10,5", "lon": -74.7}}
        Output: {"Latitude": 10.5, "Longitude": -74.7}
    """
    # Unwrap single-key nested objects
    if isinstance(raw_payload, dict) and len(raw_payload) == 1:
        only_key = next(iter(raw_payload))
        candidate = raw_payload[only_key] if isinstance(raw_payload[only_key], dict) else raw_payload
    else:
        candidate = raw_payload if isinstance(raw_payload, dict) else {}

    normalized: Dict[str, Any] = {}
    for k, v in candidate.items():
        # Map alternative field names to standard names
        mapped = _KEY_MAP.get(k, _KEY_MAP.get(k.lower(), k))
        if mapped in _ALLOWED_KEYS:
            normalized[mapped] = _coerce_number(v) if mapped != "DeviceID" else v
    
    return normalized


# ==========================================================
# Main UDP Server Loop
# ==========================================================

def udp_server():
    """
    Main UDP server loop for receiving and processing GPS data.
    
    Processing pipeline:
    1. Receive UDP packet
    2. Decode and parse JSON (with fallback strategies)
    3. Normalize field names and values
    4. Parse timestamp to UTC datetime
    5. Validate with Pydantic schema
    6. Check device registration and active status
    7. Detect geofence events (entry/exit/inside)
    8. Insert GPS data with duplicate prevention
    9. Update device LastSeen timestamp
    10. Log events via WebSocket
    
    Runs indefinitely in daemon thread.
    """
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("0.0.0.0", UDP_PORT))
    print(f"[UDP] Server listening on port {UDP_PORT}")
    log_ws.log_from_thread(f"[UDP] Server started on port {UDP_PORT}", msg_type="log")

    while True:
        try:
            data, addr = udp_sock.recvfrom(BUFFER_SIZE)
            sender_ip, sender_port = addr[0], addr[1]
            print(f"[UDP] Received {len(data)} bytes from {sender_ip}:{sender_port}")

            # ========================================
            # STEP 1: Decode JSON string
            # ========================================
            try:
                json_str = data.decode("utf-8").strip()
            except UnicodeDecodeError:
                json_str = data.decode("utf-8", errors="replace").strip()
                print(f"[UDP] Warning: decode replaced invalid bytes from {sender_ip}:{sender_port}")

            # Remove BOM if present
            json_str = json_str.lstrip("\ufeff").strip()

            # ========================================
            # STEP 2: Parse JSON with fallback strategies
            # ========================================
            try:
                raw_payload = json.loads(json_str)
            except json.JSONDecodeError:
                # Fallback 1: Extract JSON from surrounding text
                candidate = _extract_json_candidate(json_str)
                try:
                    raw_payload = json.loads(candidate)
                except json.JSONDecodeError:
                    # Fallback 2: Replace single quotes with double quotes
                    try:
                        raw_payload = json.loads(json_str.replace("'", '"'))
                    except json.JSONDecodeError as jde2:
                        print(f"[UDP] JSON decode error from {sender_ip}:{sender_port}: {jde2}")
                        log_ws.log_from_thread(
                            f"[UDP] Malformed JSON from {sender_ip}:{sender_port}: {json_str[:100]}",
                            msg_type="error"
                        )
                        continue

            # ========================================
            # STEP 3: Normalize field names and values
            # ========================================
            normalized = _normalize_payload(raw_payload)

            # ========================================
            # STEP 4: Parse timestamp to UTC datetime
            # ========================================
            ts_value = normalized.get("Timestamp")
            if ts_value is not None:
                try:
                    normalized["Timestamp"] = datetime.fromtimestamp(float(ts_value), tz=timezone.utc)
                except Exception as e:
                    print(f"[UDP] Invalid timestamp {ts_value} from {sender_ip}:{sender_port}: {e}")
                    log_ws.log_from_thread(
                        f"[UDP] Invalid timestamp {ts_value} from {sender_ip}:{sender_port}",
                        msg_type="error"
                    )
                    continue

            if not normalized:
                print(f"[UDP] Normalized payload empty from {sender_ip}:{sender_port} - skipping")
                continue

            # ========================================
            # STEP 5: Validate with Pydantic schema
            # ========================================
            try:
                gps_data = GpsData_create(**normalized)
            except ValidationError as ve:
                print(f"[UDP] ValidationError from {sender_ip}:{sender_port}: {ve}")
                print(f"[UDP] Normalized payload: {normalized}")
                log_ws.log_from_thread(
                    f"[UDP] ValidationError from {sender_ip}:{sender_port}: {ve}",
                    msg_type="error"
                )
                continue

            # ========================================
            # STEP 6: Security - Check DeviceID presence
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
            # STEP 7: Database operations (device validation + GPS insertion)
            # ========================================
            try:
                with SessionLocal() as db:
                    # --------------------------------------------
                    # Security: Check device registration & status
                    # --------------------------------------------
                    device_record = db.query(Device).filter(Device.DeviceID == device_id).first()

                    if not device_record:
                        print(f"[UDP] Unregistered device '{device_id}' from {sender_ip}:{sender_port} - REJECTED")
                        log_ws.log_from_thread(
                            f"[UDP] SECURITY: Rejected GPS from unregistered device '{device_id}' (IP: {sender_ip}:{sender_port})",
                            msg_type="error"
                        )
                        continue

                    if device_record.IsActive is False:
                        print(f"[UDP] Inactive device '{device_id}' from {sender_ip}:{sender_port} - REJECTED")
                        log_ws.log_from_thread(
                            f"[UDP] SECURITY: Rejected GPS from inactive device '{device_id}' (IP: {sender_ip}:{sender_port})",
                            msg_type="error"
                        )
                        continue

                    # ✅ Device is valid - proceed with GPS insertion
                    try:
                        incoming_dict = gps_data.model_dump()
                        log_ws.log_from_thread(
                            f"[UDP] Device '{device_id}' from {sender_ip}: {incoming_dict}",
                            msg_type="log"
                        )

                        # ========================================
                        # STEP 8: Geofence detection with EXIT event handling
                        # ========================================
                        try:
                            # Get previous GPS to detect geofence transitions
                            previous_gps = get_last_gps_row_by_device(db, device_id)
                            
                            # Detect current geofence status
                            geofence_info = geofence_detector.check_point(
                                db=db,
                                device_id=device_id,
                                lat=gps_data.Latitude,
                                lon=gps_data.Longitude,
                                timestamp=gps_data.Timestamp
                            )
                            
                            if geofence_info:
                                # 🔥 CRITICAL: Handle direct transitions between geofences
                                # If entering new geofence while still in another, create EXIT event
                                if (
                                    geofence_info['event_type'] == 'entry' and 
                                    previous_gps and 
                                    previous_gps.get('CurrentGeofenceID')
                                ):
                                    # Create artificial EXIT record 1 microsecond before ENTRY
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

                                # Set geofence fields for current GPS
                                incoming_dict['CurrentGeofenceID'] = geofence_info['id']
                                incoming_dict['CurrentGeofenceName'] = geofence_info['name']
                                incoming_dict['GeofenceEventType'] = geofence_info['event_type']

                                # Log only ENTRY/EXIT events (not every 'inside' point)
                                if geofence_info['event_type'] in ('entry', 'exit'):
                                    action = "ENTERED" if geofence_info['event_type'] == 'entry' else "EXITED"
                                    
                                    # For EXIT, use previous geofence name
                                    if geofence_info['event_type'] == 'exit':
                                        geo_name = previous_gps.get('CurrentGeofenceName', 'Unknown Zone') if previous_gps else 'Unknown Zone'
                                    else:
                                        geo_name = geofence_info.get('name', 'Unknown')
                                    
                                    log_ws.log_from_thread(
                                        f"[GEOFENCE] {device_id} {action} {geo_name}",
                                        msg_type="log"
                                    )

                            else:
                                # GPS is outside all geofences
                                incoming_dict['CurrentGeofenceID'] = None
                                incoming_dict['CurrentGeofenceName'] = None
                                incoming_dict['GeofenceEventType'] = None
                                
                        except Exception as geo_error:
                            print(f"[UDP] Geofence detection error for {device_id}: {geo_error}")
                            log_ws.log_from_thread(
                                f"[UDP] Geofence detection error for {device_id}: {geo_error}",
                                msg_type="error"
                            )
                            # Continue without geofence data
                            incoming_dict['CurrentGeofenceID'] = None
                            incoming_dict['CurrentGeofenceName'] = None
                            incoming_dict['GeofenceEventType'] = None

                        # ========================================
                        # STEP 9: Insert GPS data
                        # ========================================
                        new_row = created_gps_data(db, GpsData_create(**incoming_dict))

                        # ========================================
                        # STEP 10: Update device LastSeen timestamp
                        # ========================================
                        device_record.LastSeen = gps_data.Timestamp
                        db.commit()

                        log_ws.log_from_thread(
                            f"[UDP] Device '{device_id}': GPS inserted successfully (DB ID: {new_row.id})",
                            msg_type="log"
                        )

                    except Exception as insert_error:
                        db.rollback()
                        error_str = str(insert_error).lower()

                        # Handle duplicate GPS (unique constraint violation)
                        if "unique_device_timestamp" in error_str or "duplicate key" in error_str:
                            print(f"[UDP] Device '{device_id}': Duplicate GPS (DeviceID+Timestamp) - skipped")
                            # Not an error - normal in multi-backend setups
                        else:
                            print(f"[UDP] Device '{device_id}': Unexpected DB error: {insert_error}")
                            log_ws.log_from_thread(
                                f"[UDP] DB error for device '{device_id}': {insert_error}",
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
            log_ws.log_from_thread(f"[UDP] Critical server error: {e}", msg_type="error")


# ==========================================================
# Public API
# ==========================================================

def start_udp_server() -> threading.Thread:
    """
    Start UDP server in a background daemon thread.
    
    Returns:
        Thread object for the UDP server
        
    Example:
        # In main.py
        from src.Services.udp import start_udp_server
        
        udp_thread = start_udp_server()
    """
    thread = threading.Thread(target=udp_server, daemon=True, name="UDP-Server")
    thread.start()
    print("[UDP] Background thread started")
    log_ws.log_from_thread("[UDP] Background thread started", msg_type="log")
    return thread