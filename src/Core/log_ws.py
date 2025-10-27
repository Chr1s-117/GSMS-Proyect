# src/Core/log_ws.py

from typing import Dict, Any
from .wsBase import WebSocketManager
from fastapi import WebSocket

class LogWebSocketManager(WebSocketManager):
    """
    Specialized WebSocket manager for handling log/error connections.

    Extends the base WebSocketManager to support processing
    incoming messages from log clients.

    Responsibilities:
    - Manage log WebSocket connections.
    - Broadcast log messages in a thread-safe manner.
    - Optional future extensions: log level filtering, client subscriptions, remote control commands.
    """

    @property
    def has_clients(self) -> bool:
        """
        Returns True if at least one log client is connected.
        """
        return len(self.clients) > 0

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming messages from log WebSocket clients.

        Args:
            ws: WebSocket connection that sent the message.
            message: Text message received from the client.

        Notes:
            - Currently, this method only prints the received message.
            - Future improvements may include filtering by log level,
              selective client subscriptions, or remote control commands.
        """
        print(f"[LOG-WS] Received message: {message}")
        # TODO: Implement custom logic if required


# Dedicated instance of LogWebSocketManager for broadcasting logs
log_ws_manager = LogWebSocketManager()


def log_from_thread(message: str, msg_type: str = "log"):
    """
    Thread-safe entry point to broadcast log messages to all connected clients.

    Args:
        message: The log text to broadcast.
        msg_type: Type of the message, typically "log" or "error".

    Notes:
        - Messages are only sent if there is at least one connected client.
        - Uses the main FastAPI event loop via WebSocketManager.send_from_thread().
    """
    if log_ws_manager.has_clients:
        payload: Dict[str, Any] = {"msg_type": msg_type, "message": str(message)}
        log_ws_manager.send_from_thread(payload)
    else:
        print(f"[LOG-BROADCAST] No log clients connected. Message: {message}")