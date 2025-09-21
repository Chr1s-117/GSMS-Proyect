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
from datetime import datetime, timezone
from src.Repositories import gps_data as gps_repo
from src.DB.session import SessionLocal
from src.Schemas.gps_data import GpsData_get
from src.Core import log_ws
from src.Core import gps_ws


def _timestamp_to_iso(ts: Optional[datetime]) -> Optional[str]:
    """
    Convert a UTC-aware datetime object to an ISO 8601 string with 'Z' suffix.

    Args:
        ts (Optional[datetime]): UTC-aware datetime object.

    Returns:
        Optional[str]: ISO 8601 formatted string, or None if input is invalid.
    """
    if ts is None:
        return None
    if isinstance(ts, datetime):
        return ts.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return None


def fetch_latest_gps_data() -> Optional[Dict[str, Any]]:
    """
    Fetch the most recent GPS row from the database.

    - Converts the database model to a dictionary suitable for WebSocket broadcast.
    - Removes internal database identifiers.
    - Converts the timestamp to ISO 8601 format.

    Returns:
        Optional[Dict[str, Any]]: Latest GPS data dictionary, or None if no data is available.
    """
    try:
        with SessionLocal() as db:
            last_row = gps_repo.get_last_gps_row(db)
            if last_row is None:
                return None

            # Validate and serialize using Pydantic schema
            pydantic_row = GpsData_get.model_validate(last_row)
            data = pydantic_row.model_dump()

            # Remove internal database ID
            data.pop("id", None)
            data["Timestamp"] = _timestamp_to_iso(data.get("Timestamp"))

            return data

    except Exception as ex:
        # Log database retrieval errors from the thread context
        log_ws.log_from_thread(f"[GPS-BROADCAST] Error fetching latest GPS data: {ex}", msg_type="error")
        return None


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
            data_to_send = fetch_latest_gps_data()

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
