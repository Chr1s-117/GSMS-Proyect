# src/Services/udp.py
"""
UDP Server for receiving GPS and Accelerometer data from devices.
✨ REFACTORED VERSION - Clean orchestrator pattern

This is a clean orchestrator that delegates all processing logic to specialized modules:
- udp_core: Parsing, normalization, validation
- event_handlers: Geofence detection, trip management, persistence

Reduced from ~600 lines to ~150 lines (75% reduction) while maintaining all functionality.
"""

import socket
import threading
import os

# Core imports
from src.DB.session import SessionLocal
from src.Core import log_ws
from src.Repositories.gps_data import get_last_gps_row_by_device
from src.Repositories.trip import get_active_trip_by_device

# Schemas
from src.Schemas.gps_data import GpsData_create
from src.Schemas.accelerometer_data import AccelData_create

# UDP processing modules
from src.Services.udp_core import (
    parse_udp_packet,
    normalize_timestamp,
    normalize_gps_payload,
    extract_accel_data,
    validate_device,
    validate_gps_schema,
    validate_accel_schema
)

# Event handlers
from src.Services.event_handlers import (
    handle_geofence_detection,
    handle_trip_detection,
    insert_data
)


# ==========================================================
# UDP CONFIGURATION
# ==========================================================
UDP_PORT = int(os.getenv("UDP_PORT", "9001"))
BUFFER_SIZE = 65535  # maximum safe UDP packet size


# ==========================================================
# UDP SERVER MAIN LOOP
# ==========================================================
def udp_server():
    """
    Main UDP server loop - Clean orchestrator pattern.
    
    Flow:
    1. Parse UDP packet
    2. Normalize GPS payload
    3. Validate GPS schema
    4. Extract & validate Accel data (optional)
    5. Validate device in DB
    6. Handle geofence detection
    7. Handle trip detection
    8. Persist to database
    
    All complex logic is delegated to specialized handlers.
    This function only orchestrates the flow.
    """
    # Setup socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("0.0.0.0", UDP_PORT))
    print(f"[UDP] Server listening on port {UDP_PORT}")

    while True:
        try:
            # ========================================
            # RECEIVE PACKET
            # ========================================
            data, addr = udp_sock.recvfrom(BUFFER_SIZE)
            sender_ip, sender_port = addr[0], addr[1]
            print(f"[UDP] Received {len(data)} bytes from {sender_ip}:{sender_port}")

            # ========================================
            # PASO 1: PARSE UDP PACKET
            # ========================================
            try:
                raw_payload = parse_udp_packet(data, sender_ip, sender_port)
            except ValueError as e:
                print(f"[UDP] Parse error from {sender_ip}:{sender_port}: {e}")
                continue

            # ========================================
            # PASO 2: NORMALIZE GPS PAYLOAD
            # ========================================
            normalized = normalize_gps_payload(raw_payload)
            
            if not normalized:
                print(f"[UDP] Empty payload from {sender_ip}:{sender_port} - skipping")
                continue

            # Normalize timestamp
            ts_value = normalized.get("Timestamp")
            if ts_value is not None:
                try:
                    normalized["Timestamp"] = normalize_timestamp(ts_value)
                except ValueError as e:
                    print(f"[UDP] Invalid timestamp from {sender_ip}:{sender_port}: {e}")
                    continue

            # ========================================
            # PASO 3: VALIDATE GPS SCHEMA
            # ========================================
            gps_data = validate_gps_schema(GpsData_create, normalized, sender_ip, sender_port)
            if not gps_data:
                continue

            device_id = normalized.get("DeviceID")
            if not device_id:
                print(f"[UDP] Missing DeviceID from {sender_ip}:{sender_port} - REJECTED")
                log_ws.log_from_thread(
                    f"[UDP] SECURITY: Rejected packet without DeviceID from {sender_ip}:{sender_port}",
                    msg_type="error"
                )
                continue

            # ========================================
            # PASO 4: EXTRACT & VALIDATE ACCEL DATA (OPTIONAL)
            # ========================================
            accel_data = None
            if 'accel' in raw_payload:
                accel_dict = extract_accel_data(raw_payload, device_id, gps_data.Timestamp)
                if accel_dict:
                    accel_data = validate_accel_schema(AccelData_create, accel_dict, device_id)

            # ========================================
            # PASO 5: VALIDATE DEVICE IN DB
            # ========================================
            with SessionLocal() as db:
                device_record = validate_device(db, device_id, sender_ip, sender_port)
                if not device_record:
                    continue

                # Log incoming data
                incoming_dict = gps_data.model_dump()
                log_ws.log_from_thread(
                    f"[UDP] Device '{device_id}' from {sender_ip}: GPS={incoming_dict}, Accel={'present' if accel_data else 'none'}",
                    msg_type="log"
                )

                # Get previous GPS for context
                previous_gps = get_last_gps_row_by_device(db, device_id)

                # ========================================
                # PASO 6: HANDLE GEOFENCE DETECTION
                # ========================================
                geofence_fields = handle_geofence_detection(
                    db=db,
                    device_id=device_id,
                    latitude=gps_data.Latitude,
                    longitude=gps_data.Longitude,
                    altitude=gps_data.Altitude,
                    accuracy=gps_data.Accuracy,
                    timestamp=gps_data.Timestamp,
                    previous_gps=previous_gps
                )

                # Update GPS data with geofence fields
                gps_dict = gps_data.model_dump()
                gps_dict.update(geofence_fields)
                gps_data = GpsData_create(**gps_dict)

                # ========================================
                # PASO 7: HANDLE TRIP DETECTION
                # ========================================
                active_trip = get_active_trip_by_device(db, device_id)
                
                current_gps = {
                    'Latitude': gps_data.Latitude,
                    'Longitude': gps_data.Longitude,
                    'Timestamp': gps_data.Timestamp
                }
                
                trip_id = handle_trip_detection(
                    db=db,
                    device_id=device_id,
                    current_gps=current_gps,
                    previous_gps=previous_gps,
                    active_trip=active_trip
                )

                # ========================================
                # PASO 8: PERSIST TO DATABASE
                # ========================================
                gps_inserted, accel_inserted = insert_data(
                    db=db,
                    gps_data=gps_data,
                    accel_data=accel_data,
                    device_record=device_record,
                    trip_id=trip_id
                )

                if not gps_inserted:
                    # GPS duplicado - continuar con siguiente paquete
                    print(f"[UDP] Device '{device_id}': GPS not inserted (duplicate)")
                    continue

        except Exception as e:
            print(f"[UDP] Critical error processing packet: {e}")
            log_ws.log_from_thread(
                f"[UDP] Critical error: {e}",
                msg_type="error"
            )



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