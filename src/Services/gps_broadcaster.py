# src/Services/gps_broadcaster.py

"""
GPS Broadcaster Service (Real-Time) with Change Detection

Responsibilities:
- Continuously fetch the latest GPS data from the database.
- Convert timestamps to ISO 8601 (UTC) format.
- Broadcast data over WebSocket only if it differs from the previous broadcast.
- Runs as a daemon thread to operate concurrently with other backend services.
- Logs every significant event for monitoring and debugging.
"""

import threading
from typing import Any, Dict, Optional
from src.Repositories.gps_data import get_last_gps_row
from src.DB.session import SessionLocal
from src.Core import log_ws
from src.Core import gps_ws

def broadcast_loop():
    """
    Core loop for broadcasting GPS data to WebSocket clients.

    Behavior:
    - Continuously fetches the latest GPS data.
    - Only broadcasts if the data has changed since the last sent payload.
    - Requires at least one connected client for both GPS and log WebSocket managers.
    - Runs indefinitely inside a daemon thread.
    """
    last_sent_row: Optional[Dict[str, Any]] = None

    while True:
        try:
            with SessionLocal() as db:
                # get_last_gps_row already returns dict | None, serialized with ISO timestamp and no ID
                data_to_send = get_last_gps_row(db)

            if data_to_send is not None:
                # Only send if the data has changed
                if data_to_send != last_sent_row and gps_ws.gps_ws_manager.has_clients and log_ws.log_ws_manager.has_clients:
                    print(f"[GPS-BROADCAST*] Sent GPS data: {data_to_send}")
                    gps_ws.gps_from_thread(data_to_send)
                    log_ws.log_from_thread(f"[GPS-BROADCAST] Sent GPS data: {data_to_send}", msg_type="log")
                    last_sent_row = data_to_send

        except Exception as ex:
            # Catch any unexpected errors to prevent thread crash
            log_ws.log_from_thread(f"[GPS-BROADCAST] Error in broadcast_loop: {ex}", msg_type="error")


def start_gps_broadcaster() -> threading.Thread:
    """
    Initialize and start the GPS broadcaster as a daemon thread.

    Returns:
        threading.Thread: Reference to the running daemon thread.
    """
    thread = threading.Thread(target=broadcast_loop, daemon=True, name="GPS-Broadcaster")
    thread.start()
    log_ws.log_from_thread("[GPS-BROADCAST] Started broadcast thread", msg_type="log")
    return thread