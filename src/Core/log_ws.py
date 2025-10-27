# src/Core/log_ws.py

"""
Log WebSocket Manager

Manages WebSocket connections for real-time log/error broadcasting.

Features:
- Thread-safe log broadcasting
- Client connection tracking
- Message type support (log, error, warning)
- Automatic message routing to all connected clients

Integration:
- Used throughout the application for centralized logging
- Broadcasts to admin dashboard/debug console
- Can filter by log level in future versions

Usage:
    from src.Core.log_ws import log_from_thread
    
    log_from_thread("GPS data received from TRUCK-001", msg_type="log")
    log_from_thread("Database connection failed", msg_type="error")

Created: 2025-10-27
"""

from typing import Dict, Any
from .wsBase import WebSocketManager
from fastapi import WebSocket


class LogWebSocketManager(WebSocketManager):
    """
    Specialized WebSocket manager for handling log/error connections.

    Extends the base WebSocketManager to support processing
    incoming messages from log clients.

    Responsibilities:
    - Manage log WebSocket connections
    - Broadcast log messages in a thread-safe manner
    - Optional future extensions: log level filtering, client subscriptions
    """

    @property
    def has_clients(self) -> bool:
        """
        Returns True if at least one log client is connected.
        
        Used to avoid sending logs when no admin/debug clients are connected.
        """
        return len(self.clients) > 0

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming messages from log WebSocket clients.

        Args:
            ws: WebSocket connection that sent the message
            message: Text message received from the client

        Notes:
            Currently only prints received messages.
            Future improvements may include:
            - Filtering by log level
            - Selective client subscriptions
            - Remote control commands (e.g., change log level)
        """
        print(f"[LOG-WS] Received message: {message}")
        # TODO: Implement custom logic if required (e.g., log level filtering)


# ==========================================================
# Global Singleton Instance
# ==========================================================

# Dedicated instance of LogWebSocketManager for broadcasting logs
log_ws_manager = LogWebSocketManager()


# ==========================================================
# Thread-Safe Public API
# ==========================================================

def log_from_thread(message: str, msg_type: str = "log"):
    """
    Thread-safe entry point to broadcast log messages to all connected clients.

    This function can be safely called from any thread (UDP receiver,
    background tasks, services, etc.) and will properly schedule the
    broadcast on the main FastAPI event loop.

    Args:
        message: The log text to broadcast
        msg_type: Type of the message - "log" | "error" | "warning" | "info"
            - "log": General informational messages (default)
            - "error": Error messages (red in UI)
            - "warning": Warning messages (yellow in UI)
            - "info": Info messages (blue in UI)

    Returns:
        None

    Example:
        from src.Core.log_ws import log_from_thread
        
        log_from_thread("GPS data received from TRUCK-001", msg_type="log")
        log_from_thread("Database connection failed", msg_type="error")
        log_from_thread("UDP packet size exceeds limit", msg_type="warning")

    Notes:
        - Messages are only sent if there is at least one connected client
        - Uses asyncio.call_soon_threadsafe for thread safety
        - Non-blocking (returns immediately)
    
    Performance:
        - Typical latency: <5ms from call to WebSocket send
        - No performance impact if no clients connected
    """
    if log_ws_manager.has_clients:
        payload: Dict[str, Any] = {
            "msg_type": msg_type,
            "message": str(message)
        }
        log_ws_manager.send_from_thread(payload)
    else:
        # Uncomment for debugging:
        # print(f"[LOG-BROADCAST] No log clients connected. Message: {message}")
        pass