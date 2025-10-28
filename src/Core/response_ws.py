# src/Core/response_ws.py
from typing import Dict, Any
from .wsBase import WebSocketManager
from fastapi import WebSocket

class ResponseWebSocketManager(WebSocketManager):
    """
    Specialized WebSocket manager for Response connections.
    Provides:
      - has_clients property to check for connected clients.
      - Thread-safe sending with logging.
      - Extensible message handler if needed in the future.
    """

    @property
    def has_clients(self) -> bool:
        """Return True if at least one client is connected."""
        return len(self.clients) > 0

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming messages from Response WebSocket clients.
        Currently logs received messages.
        """
        print(f"[RESPONSE-WS] Received message from client: {message}")
        # Future: parse commands or handle client-specific subscriptions

# --- Dedicated manager instance ---
response_ws_manager = ResponseWebSocketManager()

def response_from_thread(data: Dict[str, Any]):
    """
    Thread-safe method to broadcast a response to all connected clients.
    Use this function in place of direct `send_from_thread` calls.
    """
    print(f"[RESPONSE-WS] has_clients={response_ws_manager.has_clients}")
    if response_ws_manager.has_clients:
        print(f"[RESPONSE-WS] Sending response: {data}")
        response_ws_manager.send_from_thread(data)
    else:
        print("[RESPONSE-WS] No clients connected. Response not sent.")
