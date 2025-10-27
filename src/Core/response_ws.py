# src/Core/response_ws.py

"""
Response WebSocket Manager

Manages WebSocket connections for broadcasting request responses to clients.

This manager handles the response channel in the request-response pattern:
1. Client sends request via request_ws.py
2. Request is processed by request_handlers.py
3. Response is queued in response_broadcaster.py
4. Response is sent via this manager to response_ws clients

Features:
- Thread-safe response broadcasting
- Client connection tracking
- Request-response correlation via request_id
- Automatic message routing to all connected clients

Integration:
- Used by response_broadcaster.py to send responses
- Receives responses from request handlers
- Broadcasts to frontend clients waiting for responses

Usage:
    from src.Core.response_ws import response_from_thread
    
    response_dict = {
        "action": "get_devices",
        "request_id": "req-12345",
        "status": "success",
        "data": {"devices": [...], "count": 25}
    }
    
    response_from_thread(response_dict)  # Thread-safe broadcast

Created: 2025-10-27
Author: Chr1s-117
"""

from typing import Dict, Any
from .wsBase import WebSocketManager
from fastapi import WebSocket


class ResponseWebSocketManager(WebSocketManager):
    """
    Specialized WebSocket manager for Response connections.
    
    Extends WebSocketManager with:
    - has_clients property to check for connected clients
    - Conditional sending from threads based on connected clients
    - Message handling for future client commands (if needed)
    """

    @property
    def has_clients(self) -> bool:
        """
        Returns True if at least one response client is connected.
        
        Used by response_broadcaster to avoid sending responses
        when no clients are waiting.
        
        Returns:
            bool: True if clients connected, False otherwise
        """
        return len(self.clients) > 0

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming messages from Response WebSocket clients.
        
        Currently logs received messages. Can be extended for:
        - Request cancellation
        - Response acknowledgment
        - Client-specific filtering
        - Priority queuing
        
        Args:
            ws: WebSocket connection that sent the message
            message: Text message received from client
        """
        print(f"[RESPONSE-WS] 📨 Received message from client: {message}")
        # Future: parse commands or handle client-specific subscriptions


# ==========================================================
# Global Singleton Instance
# ==========================================================

# Dedicated manager instance for response broadcasting
response_ws_manager = ResponseWebSocketManager()


# ==========================================================
# Thread-Safe Public API
# ==========================================================

def response_from_thread(data: Dict[str, Any]):
    """
    Thread-safe method to broadcast a response to all connected clients.
    
    This function can be safely called from any thread (UDP receiver,
    background tasks, request handlers) and will properly schedule the
    broadcast on the main FastAPI event loop.
    
    Args:
        data: Response data dictionary with structure:
            {
                "action": "get_devices",
                "request_id": "req-12345",
                "status": "success" | "error",
                "data": {...}
            }
    
    Returns:
        None
    
    Example:
        from src.Core.response_ws import response_from_thread
        
        response_dict = {
            "action": "get_devices",
            "request_id": "req-12345",
            "status": "success",
            "data": {"devices": ["TRUCK-001"], "count": 1}
        }
        
        response_from_thread(response_dict)  # Broadcasts to all response clients
    
    Performance:
        - Only sends if clients are connected (avoids unnecessary work)
        - Uses asyncio.call_soon_threadsafe for thread safety
        - Non-blocking (returns immediately)
    
    Integration:
        - Called by response_broadcaster.py after response_ws_manager.has_clients check
        - Coordinates with request_ws.py for request-response correlation
    """
    print(f"[RESPONSE-WS] 🔍 has_clients={response_ws_manager.has_clients}")
    
    if response_ws_manager.has_clients:
        print(f"[RESPONSE-WS] 📤 Sending response: {data}")
        response_ws_manager.send_from_thread(data)
    else:
        print("[RESPONSE-WS] ⚠️  No clients connected. Response not sent.")