from typing import Dict, Any
from .wsBase import WebSocketManager
from fastapi import WebSocket

class GpsWebSocketManager(WebSocketManager):
    """
    Specialized WebSocket manager for GPS connections.
    Extends WebSocketManager with:
      - has_clients property to know if clients are connected.
      - Conditional sending from threads based on connected clients.
    """

    @property
    def has_clients(self) -> bool:
        """
        Returns True if at least one client is connected.
        """
        return len(self.clients) > 0

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming messages from GPS WebSocket clients.
        Currently logs received messages, can be extended later.
        """
        print(f"[GPS-WS] Received message: {message}")
        # Future: handle commands, update frequency, client preferences, etc.

# Dedicated GPS WebSocket manager instance
gps_ws_manager = GpsWebSocketManager()

def gps_from_thread(data: Dict[str, Any]):
    """
    Thread-safe entry point to broadcast GPS data to all connected clients.
    Only sends if there is at least one client connected.
    """
    if gps_ws_manager.has_clients:
        gps_ws_manager.send_from_thread(data)
    else:
        print("[GPS-WS] No clients connected. Data not sent.")
