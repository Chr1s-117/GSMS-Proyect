# src/Services/gps_broadcaster.py

"""
GPS Broadcaster Service with Change Detection (Real-Time)

- Continuously fetches the latest GPS data from the database.
- Sends the data via WebSocket only if it has changed since the last broadcast.
- Operates in a daemon thread to run in parallel with the backend services.
"""

import threading
from typing import Optional, Dict
from src.Repositories.gps_data import get_last_gps_row
from src.DB.session import SessionLocal
from src.Core import log_ws, gps_ws


def broadcast_loop():
    """
    Main loop that continuously fetches the latest GPS data
    and sends it via WebSocket only if it has changed.
    Runs indefinitely in a daemon thread.
    """
    last_sent_row: Optional[Dict[str, str | float]] = None

    while True:
        try:
            with SessionLocal() as db:
                # get_last_gps_row already returns dict | None
                data_to_send = get_last_gps_row(db)

            if data_to_send is not None:
                # Send only if the data has changed since the last broadcast
                if (
                    data_to_send != last_sent_row
                    and gps_ws.gps_ws_manager.has_clients
                    and log_ws.log_ws_manager.has_clients
                ):
                    print(f"[GPS-BROADCAST*] Sent GPS data: {data_to_send}")
                    gps_ws.gps_from_thread(data_to_send)
                    log_ws.log_from_thread(
                        f"[GPS-BROADCAST] Sent GPS data: {data_to_send}",
                        msg_type="log"
                    )
                    last_sent_row = data_to_send

        except Exception as ex:
            log_ws.log_from_thread(
                f"[GPS-BROADCAST] Error in broadcast_loop: {ex}",
                msg_type="error"
            )


def start_gps_broadcaster() -> threading.Thread:
    """
    Launches the GPS broadcaster in a daemon thread.
    Returns the thread object for reference if needed.
    """
    thread = threading.Thread(
        target=broadcast_loop,
        daemon=True,
        name="GPS-Broadcaster"
    )
    thread.start()

    print("[GPS-BROADCAST] Started broadcast thread")
    return thread
