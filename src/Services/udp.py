# src/Services/udp.py

"""
UDP Server Service for GPS Data Reception

This module implements a high-performance UDP server designed to handle
real-time GPS packets sent by devices. It ensures data integrity,
normalization, device validation, geofence detection, and centralized logging.

Key Features (v2.0):
- Multi-device support with DeviceID field
- Device validation (registered + active)
- Geofence detection with entry/exit/inside events
- Automatic EXIT event generation on geofence transitions
- Duplicate prevention via database unique constraint
- LastSeen timestamp updates for devices
- Centralized logging through log_ws
- Runs in daemon thread asynchronously

Packet Format:
    Expected JSON format from GPS devices:
    {
        "DeviceID": "TRUCK-001",
        "Latitude": 10.9878,
        "Longitude": -74.7889,
        "Altitude": 50.0,
        "Accuracy": 5.0,
        "Timestamp": 1706332851
    }

Security:
    - Only registered devices can send GPS data
    - Inactive devices are rejected
    - Unregistered devices are logged as security events
    - DeviceID is mandatory for all packets

Environment Configuration:
    UDP_PORT: UDP listening port (default: 9001)
    DISABLE_UDP: Set to "1" to disable UDP service (default: 0)

Usage:
    # In main.py lifespan
    if settings.UDP_ENABLED:
        from src.Services.udp import start_udp_server
        udp_thread = start_udp_server()
"""

import socket
import json
import threading
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from pydantic import ValidationError

# Database and models
from src.DB.session import SessionLocal
from src.Models.device import Device
from src.Schemas.gps_data import GpsData_create

# Repositories
from src.Repositories.gps_data import created_gps_data, get_last_gps_row_by_device

# Services
from src.Services.geofence_detector import geofence_detector
from src.Core import log_ws


# ==========================================================
# 📌 UDP Server Configuration
# ==========================================================

UDP_PORT = int(os.getenv("UDP_PORT", "9001"))
BUFFER_SIZE = 65535  # Maximum safe UDP packet size (64KB)

# Allowed GPS data fields
_ALLOWED_KEYS = {"DeviceID", "Latitude", "Longitude", "Altitude", "Accuracy", "Timestamp"}

# Key normalization map (handles different naming conventions)
_KEY_MAP = {
    # Device ID variants
    "device_id": "DeviceID",
    "deviceId": "DeviceID",
    "deviceid": "DeviceID",
    "device": "DeviceID",
    "DeviceID": "DeviceID",

    # GPS coordinate variants
    "latitude": "Latitude", "lat": "Latitude", "Latitude": "Latitude",
    "longitude": "Longitude", "lon": "Longitude", "lng": "Longitude", "Longitude": "Longitude",
    "altitude": "Altitude", "alt": "Altitude", "Altitude": "Altitude",
    "accuracy": "Accuracy", "acc": "Accuracy", "Accuracy": "Accuracy",

    # Timestamp variants
    "timestamp": "Timestamp", "time": "Timestamp", "timeStamp": "Timestamp", "Timestamp": "Timestamp",
}


# ==========================================================
# 📌 JSON Parsing and Normalization Helpers
# ==========================================================

def _extract_json_candidate(s: str) -> str:
    """
    Extract JSON object from string that may contain garbage.
    
    Handles cases where UDP packet contains extra characters
    before/after the JSON payload.
    
    Args:
        s: Raw string data
        
    Returns:
        Extracted JSON substring
        
    Example:
        "garbage{\"lat\":10.5}trash" → "{\"lat\":10.5}"
    """
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1 and end > start:
        return s[start:end+1]
    return s


def _coerce_number(value: Any) -> Optional[float]:
    """
    Coerce various input formats to float.
    
    Handles:
    - String numbers with commas as decimal separator ("10,5" → 10.5)
    - Empty strings and "null" strings (→ None)
    - Already-numeric values (pass through)
    
    Args:
        value: Input value of any type
        
    Returns:
        Float value or None
        
    Example:
        "10,5" → 10.5
        "null" → None
        10.5 → 10.5
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        v = value.strip()
        if v == "" or v.lower() == "null":
            return None
        v = v.replace(",", ".")  # Handle European decimal separator
        try:
            return float(v)
        except ValueError:
            return value
    return value


def _normalize_payload(raw_payload: Any) -> Dict[str, Any]:
    """
    Normalize incoming JSON payload to standard schema format.
    
    Handles:
    - Nested payloads (unwraps single-key dicts)
    - Case-insensitive field names
    - Various field name conventions (lat/latitude, lon/longitude, etc.)
    - Numeric coercion (strings to floats)
    
    Args:
        raw_payload: Parsed JSON object (dict)
        
    Returns:
        Normalized dict with standardized keys
        
    Example:
        {"device": "T1", "lat": "10,5", "lon": -74.7}
        →
        {"DeviceID": "T1", "Latitude": 10.5, "Longitude": -74.7}
    """
    # Unwrap single-key nested dicts
    if isinstance(raw_payload, dict) and len(raw_payload) == 1:
        only_key = next(iter(raw_payload))
        candidate = raw_payload[only_key] if isinstance(raw_payload[only_key], dict) else raw_payload
    else:
        candidate = raw_payload if isinstance(raw_payload, dict) else {}

    # Normalize keys and coerce values
    normalized: Dict[str, Any] = {}
    for k, v in candidate.items():
        mapped = _KEY_MAP.get(k, _KEY_MAP.get(k.lower(), k))
        if mapped in _ALLOWED_KEYS:
            # Apply numeric coercion to GPS coordinates
            if mapped in ("Latitude", "Longitude", "Altitude", "Accuracy"):
                normalized[mapped] = _coerce_number(v)
            else:
                normalized[mapped] = v
    
    return normalized


# ==========================================================
# 📌 Main UDP Server Loop
# ==========================================================

def udp_server():
    """
    Main UDP server loop.
    
    Continuously listens for UDP packets on configured port,
    processes GPS data, validates devices, detects geofences,
    and inserts records into database.
    
    Flow:
    1. Receive UDP packet
    2. Parse and normalize JSON
    3. Validate DeviceID field presence
    4. Check device registration and active status
    5. Detect geofence containment
    6. Generate artificial EXIT event if needed
    7. Insert GPS record
    8. Update device LastSeen timestamp
    9. Broadcast to WebSocket clients
    
    Error Handling:
    - Malformed JSON: Skip packet
    - Invalid device: Reject and log security event
    - Duplicate GPS: Silently skip (handled by DB constraint)
    - Database errors: Log and continue
    """
    # Create and bind UDP socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("0.0.0.0", UDP_PORT))
    
    print(f"[UDP] ✅ Server listening on 0.0.0.0:{UDP_PORT}")
    log_ws.log_from_thread(
        f"[UDP] Server started on port {UDP_PORT}",
        msg_type="log"
    )

    while True:
        try:
            # --------------------------------------------------------
            # Step 1: Receive UDP packet
            # --------------------------------------------------------
            data, addr = udp_sock.recvfrom(BUFFER_SIZE)
            sender_ip, sender_port = addr[0], addr[1]
            print(f"[UDP] 📦 Received {len(data)} bytes from {sender_ip}:{sender_port}")

            # --------------------------------------------------------
            # Step 2: Decode and parse JSON
            # --------------------------------------------------------
            try:
                json_str = data.decode("utf-8").strip()
            except UnicodeDecodeError:
                json_str = data.decode("utf-8", errors="replace").strip()
                print(f"[UDP] ⚠️  Unicode decode error from {sender_ip}:{sender_port} (replaced invalid bytes)")

            # Remove BOM if present
            json_str = json_str.lstrip("\ufeff").strip()

            # Parse JSON with fallback strategies
            try:
                raw_payload = json.loads(json_str)
            except json.JSONDecodeError:
                # Try extracting JSON from garbage
                candidate = _extract_json_candidate(json_str)
                try:
                    raw_payload = json.loads(candidate)
                except json.JSONDecodeError:
                    # Try replacing single quotes with double quotes
                    try:
                        raw_payload = json.loads(json_str.replace("'", '"'))
                    except json.JSONDecodeError as jde:
                        print(f"[UDP] ❌ JSON parse error from {sender_ip}:{sender_port}: {jde}")
                        log_ws.log_from_thread(
                            f"[UDP] Invalid JSON from {sender_ip}:{sender_port}",
                            msg_type="error"
                        )
                        continue

            # --------------------------------------------------------
            # Step 3: Normalize payload
            # --------------------------------------------------------
            normalized = _normalize_payload(raw_payload)

            # Convert timestamp (Unix epoch → UTC datetime)
            ts_value = normalized.get("Timestamp")
            if ts_value is not None:
                try:
                    normalized["Timestamp"] = datetime.fromtimestamp(float(ts_value), tz=timezone.utc)
                except (ValueError, OSError) as e:
                    print(f"[UDP] ❌ Invalid timestamp {ts_value} from {sender_ip}:{sender_port}: {e}")
                    continue

            if not normalized:
                print(f"[UDP] ⚠️  Empty normalized payload from {sender_ip}:{sender_port} - skipping")
                continue

            # --------------------------------------------------------
            # Step 4: Validate with Pydantic schema
            # --------------------------------------------------------
            try:
                gps_data = GpsData_create(**normalized)
            except ValidationError as ve:
                print(f"[UDP] ❌ ValidationError from {sender_ip}:{sender_port}: {ve}")
                log_ws.log_from_thread(
                    f"[UDP] Invalid GPS data from {sender_ip}:{sender_port}: {ve}",
                    msg_type="error"
                )
                continue

            # --------------------------------------------------------
            # Step 5: SECURITY - Validate DeviceID presence
            # --------------------------------------------------------
            device_id = normalized.get("DeviceID")
            if not device_id:
                print(f"[UDP] 🚨 SECURITY: Missing DeviceID from {sender_ip}:{sender_port} - REJECTED")
                log_ws.log_from_thread(
                    f"[UDP] SECURITY: Rejected packet without DeviceID from {sender_ip}:{sender_port}",
                    msg_type="error"
                )
                continue

            # --------------------------------------------------------
            # Step 6: Database operations (device validation + insert)
            # --------------------------------------------------------
            try:
                with SessionLocal() as db:
                    # ----------------------------------------------
                    # SECURITY: Check device registration and status
                    # ----------------------------------------------
                    device_record = db.query(Device).filter(Device.DeviceID == device_id).first()

                    if not device_record:
                        print(f"[UDP] 🚨 SECURITY: Unregistered device '{device_id}' from {sender_ip}:{sender_port} - REJECTED")
                        log_ws.log_from_thread(
                            f"[UDP] SECURITY: Rejected GPS from unregistered device '{device_id}' (IP: {sender_ip}:{sender_port})",
                            msg_type="error"
                        )
                        continue

                    if not device_record.IsActive:
                        print(f"[UDP] 🚨 SECURITY: Inactive device '{device_id}' from {sender_ip}:{sender_port} - REJECTED")
                        log_ws.log_from_thread(
                            f"[UDP] SECURITY: Rejected GPS from inactive device '{device_id}' (IP: {sender_ip}:{sender_port})",
                            msg_type="error"
                        )
                        continue

                    # ----------------------------------------------
                    # Device is valid - proceed with GPS insertion
                    # ----------------------------------------------
                    try:
                        incoming_dict = gps_data.model_dump()
                        log_ws.log_from_thread(
                            f"[UDP] Device '{device_id}' from {sender_ip}: GPS={incoming_dict}",
                            msg_type="log"
                        )

                        # ----------------------------------------------
                        # GEOFENCE DETECTION
                        # ----------------------------------------------
                        try:
                            # Get previous GPS for transition detection
                            previous_gps = get_last_gps_row_by_device(db, device_id)
                            
                            # Detect current geofence
                            geofence_info = geofence_detector.check_point(
                                db=db,
                                device_id=device_id,
                                lat=gps_data.Latitude,
                                lon=gps_data.Longitude,
                                timestamp=gps_data.Timestamp
                            )
                            
                            if geofence_info:
                                # 🔥 CRITICAL: Generate EXIT event before ENTRY
                                if (
                                    geofence_info['event_type'] == 'entry' and 
                                    previous_gps and 
                                    previous_gps.get('CurrentGeofenceID')
                                ):
                                    # Create artificial EXIT record 1 microsecond before
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
                                        f"[GEOFENCE] 🔵 {device_id} EXITED {previous_gps['CurrentGeofenceName']}",
                                        msg_type="log"
                                    )

                                # Apply geofence info to incoming GPS
                                incoming_dict['CurrentGeofenceID'] = geofence_info['id']
                                incoming_dict['CurrentGeofenceName'] = geofence_info['name']
                                incoming_dict['GeofenceEventType'] = geofence_info['event_type']

                                # Log only ENTRY/EXIT events (not INSIDE)
                                if geofence_info['event_type'] in ('entry', 'exit'):
                                    action = "🟢 ENTERED" if geofence_info['event_type'] == 'entry' else "🔴 EXITED"
                                    geo_name = geofence_info.get('name', 'Unknown')
                                    
                                    log_ws.log_from_thread(
                                        f"[GEOFENCE] {action} {device_id} → {geo_name}",
                                        msg_type="log"
                                    )

                            else:
                                # Point is outside all geofences
                                incoming_dict['CurrentGeofenceID'] = None
                                incoming_dict['CurrentGeofenceName'] = None
                                incoming_dict['GeofenceEventType'] = None
                                
                        except Exception as geo_error:
                            print(f"[UDP] ⚠️  Geofence detection error for {device_id}: {geo_error}")
                            log_ws.log_from_thread(
                                f"[UDP] Geofence detection error for {device_id}: {geo_error}",
                                msg_type="error"
                            )
                            # Continue with null geofence info
                            incoming_dict['CurrentGeofenceID'] = None
                            incoming_dict['CurrentGeofenceName'] = None
                            incoming_dict['GeofenceEventType'] = None

                        # ----------------------------------------------
                        # Insert GPS record
                        # ----------------------------------------------
                        new_row = created_gps_data(db, GpsData_create(**incoming_dict))

                        # ----------------------------------------------
                        # Update device LastSeen timestamp
                        # ----------------------------------------------
                        device_record.LastSeen = gps_data.Timestamp
                        db.commit()

                        print(f"[UDP] ✅ Device '{device_id}': GPS inserted (DB ID: {new_row.id})")
                        log_ws.log_from_thread(
                            f"[UDP] Device '{device_id}': GPS inserted successfully (ID: {new_row.id})",
                            msg_type="log"
                        )

                    except Exception as insert_error:
                        db.rollback()
                        error_str = str(insert_error).lower()

                        # Handle duplicate GPS (from unique constraint)
                        if "unique_device_timestamp" in error_str or "duplicate key" in error_str:
                            print(f"[UDP] ℹ️  Device '{device_id}': Duplicate GPS (DeviceID+Timestamp) - skipped")
                        else:
                            print(f"[UDP] ❌ Device '{device_id}': Unexpected DB error: {insert_error}")
                            log_ws.log_from_thread(
                                f"[UDP] DB error for device '{device_id}': {insert_error}",
                                msg_type="error"
                            )

            except Exception as outer_error:
                print(f"[UDP] ❌ Critical error processing packet from {sender_ip}:{sender_port}: {outer_error}")
                log_ws.log_from_thread(
                    f"[UDP] Critical error from {sender_ip}:{sender_port}: {outer_error}",
                    msg_type="error"
                )

        except Exception as e:
            print(f"[UDP] ❌ Error in main loop: {e}")
            log_ws.log_from_thread(
                f"[UDP] Main loop error: {e}",
                msg_type="error"
            )


# ==========================================================
# 📌 Public API to Start Service
# ==========================================================

def start_udp_server() -> threading.Thread:
    """
    Launch the UDP server in a daemon thread.
    
    This function should be called from main.py's lifespan context
    if settings.UDP_ENABLED is True.
    
    Returns:
        threading.Thread: The background UDP server thread
        
    Example:
        # In main.py lifespan
        if settings.UDP_ENABLED:
            udp_thread = start_udp_server()
    
    Thread Behavior:
        - Runs as daemon (won't prevent app shutdown)
        - Named "UDP-Server" for easy identification in logs
        - Continues running until app terminates
    """
    thread = threading.Thread(
        target=udp_server,
        daemon=True,
        name="UDP-Server"
    )
    thread.start()
    
    print("[UDP] 🚀 Background thread started")
    log_ws.log_from_thread(
        "[UDP] Background server thread started",
        msg_type="log"
    )
    
    return thread