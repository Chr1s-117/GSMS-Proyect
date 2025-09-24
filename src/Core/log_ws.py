from typing import Dict, Any
from fastapi import WebSocket
from src.DB.session import SessionLocal
from .wsBase import WebSocketManager
from src.Repositories.gps_data import get_oldest_gps_row
import json


def log_from_thread(message: str, msg_type: str = "log"):
    """
    Thread-safe entry point to broadcast log messages to all connected clients.
    """
    if log_ws_manager.has_clients:
        payload: Dict[str, Any] = {"msg_type": msg_type, "message": str(message)}
        log_ws_manager.send_from_thread(payload)
    else:
        print(f"[LOG-BROADCAST] No log clients connected. Message: {message}")


class LogWebSocketManager(WebSocketManager):
    """
    Specialized WebSocket manager for handling log/error connections.
    """

    @property
    def has_clients(self) -> bool:
        """Returns True if at least one log client is connected."""
        return len(self.clients) > 0

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming messages from GPS WebSocket clients.
        Currently logs received messages, can be extended later.
        """
        print(f"[GPS-WS] Received message: {message}")
        # Future: handle commands, update frequency, client preferences, etc.


# Instancia dedicada para broadcasting de logs
log_ws_manager = LogWebSocketManager()

