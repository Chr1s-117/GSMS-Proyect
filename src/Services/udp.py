# src/Services/udp.py

"""
UDP Server for receiving GPS data from devices.

- Normalizes incoming JSON payloads to match Pydantic schemas.
- Converts timestamps to UTC-aware datetime objects.
- Avoids inserting duplicate records using last database row (already JSON dict).
- Logs all received packets centrally using log_ws.
"""

import os
import socket
import json
import threading
from datetime import datetime, timezone
from typing import Dict, Any
from pydantic import ValidationError
from src.Schemas.gps_data import GpsData_create
from src.Repositories.gps_data import created_gps_data, get_last_gps_row
from src.DB.session import SessionLocal
from src.Core import log_ws  

<<<<<<< HEAD
# --------------------------
# UDP Server Configuration
# --------------------------
UDP_PORT = 9001  # Use environment variable if set
BUFFER_SIZE = 65535  # Maximum safe UDP packet size
=======
# UDP configuration
UDP_PORT = int(os.getenv("UDP_PORT", "9001"))
BUFFER_SIZE = 65535  # maximum safe UDP packet size
>>>>>>> d0e2e63a10da92c04950a7a87b90ec5873dcecfc

_ALLOWED_KEYS = {"Latitude", "Longitude", "Altitude", "Accuracy", "Timestamp"}
_KEY_MAP = {
    "latitude": "Latitude", "lat": "Latitude",
    "longitude": "Longitude", "lon": "Longitude", "lng": "Longitude",
    "altitude": "Altitude", "alt": "Altitude",
    "accuracy": "Accuracy", "acc": "Accuracy",
    "timestamp": "Timestamp", "time": "Timestamp",
    "Latitude": "Latitude", "longitude": "Longitude",
    "timeStamp": "Timestamp",
}

def _extract_json_candidate(s: str) -> str:
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1 and end > start:
        return s[start:end+1]
    return s

def _coerce_number(value: Any):
<<<<<<< HEAD
    """
    Convert values to float if possible.
    Handles empty strings, 'null', and both period/comma decimal separators.
    Returns None for unconvertible values.
    """
=======
>>>>>>> d0e2e63a10da92c04950a7a87b90ec5873dcecfc
    if value is None: return None
    if isinstance(value, (int, float)): return value
    if isinstance(value, str):
        v = value.strip()
        if v == "" or v.lower() == "null": return None
        v = v.replace(",", ".")
        try: return float(v)
        except: return value
    return value

def _normalize_payload(raw_payload: Any) -> Dict[str, Any]:
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

def udp_server():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("0.0.0.0", UDP_PORT))
    print(f"[UDP] Server listening on port {UDP_PORT}")

    while True:
        try:
            data, addr = udp_sock.recvfrom(BUFFER_SIZE)
            sender_ip, sender_port = addr[0], addr[1]
            print(f"[UDP] Received {len(data)} bytes from {sender_ip}:{sender_port}")

            try: json_str = data.decode("utf-8").strip()
            except UnicodeDecodeError:
                json_str = data.decode("utf-8", errors="replace").strip()
                print(f"[UDP] Warning: decode replaced invalid bytes from {sender_ip}:{sender_port}")

            json_str = json_str.lstrip("\ufeff").strip()

            try: raw_payload = json.loads(json_str)
            except json.JSONDecodeError:
                candidate = _extract_json_candidate(json_str)
                try: raw_payload = json.loads(candidate)
                except json.JSONDecodeError:
                    try: raw_payload = json.loads(json_str.replace("'", '"'))
                    except json.JSONDecodeError as jde2:
                        print(f"[UDP] JSON decode error from {sender_ip}:{sender_port}: {jde2}")
                        continue

            normalized = _normalize_payload(raw_payload)

            ts_value = normalized.get("Timestamp")
            if ts_value is not None:
                try: normalized["Timestamp"] = datetime.fromtimestamp(float(ts_value), tz=timezone.utc)
                except Exception as e:
                    print(f"[UDP] Invalid timestamp {ts_value} from {sender_ip}:{sender_port}: {e}")
                    continue

            if not normalized:
                print(f"[UDP] Normalized payload empty from {sender_ip}:{sender_port} - skipping")
                continue

            try: gps_data = GpsData_create(**normalized)
            except ValidationError as ve:
                print(f"[UDP] ValidationError from {sender_ip}:{sender_port}: {ve} | normalized: {normalized}")
                continue

            try:
                with SessionLocal() as db:
                    last_row = get_last_gps_row(db)  # dict | None
                    incoming_dict = gps_data.dict()
<<<<<<< HEAD
=======

>>>>>>> d0e2e63a10da92c04950a7a87b90ec5873dcecfc
                    is_duplicate = last_row and all(
                        last_row.get(k) == incoming_dict.get(k)
                        for k in _ALLOWED_KEYS
                    )

<<<<<<< HEAD
                    # Centralized logging
=======
>>>>>>> d0e2e63a10da92c04950a7a87b90ec5873dcecfc
                    log_ws.log_from_thread(f"[UDP] from {sender_ip} get: {incoming_dict}", msg_type="log")

                    if is_duplicate:
                        print(f"[UDP] Duplicate data from {sender_ip}, discarded.")
                        continue

<<<<<<< HEAD
                    # Insert new GPS row
=======
>>>>>>> d0e2e63a10da92c04950a7a87b90ec5873dcecfc
                    new_row = created_gps_data(db, gps_data)
                    log_ws.log_from_thread(f"[UDP] inserted row: {new_row}", msg_type="log")

            except Exception as db_e:
                log_ws.log_from_thread(
                    f"[UDP] DB insert error from {sender_ip}: {db_e} | payload: {normalized}",
                    msg_type="error"
                )

        except Exception as e:
            print(f"[UDP] Error receiving/processing data: {e}")

def start_udp_server() -> threading.Thread:
    thread = threading.Thread(target=udp_server, daemon=True, name="UDP-Server")
    thread.start()
    print("[UDP] Background thread started")
<<<<<<< HEAD
    return thread
=======
    return thread
>>>>>>> d0e2e63a10da92c04950a7a87b90ec5873dcecfc
