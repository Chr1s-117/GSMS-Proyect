# src/Core/gps_ws.py

"""
GPS WebSocket Manager

Manages WebSocket connections for real-time GPS data broadcasting.

Features:
- Thread-safe GPS data broadcasting
- Client connection tracking
- Automatic message routing to all connected clients

Integration:
- Used by gps_broadcaster.py to send GPS updates
- Receives data from UDP receiver and HTTP endpoints
- Broadcasts to frontend map/dashboard clients

Usage:
    from src.Core.gps_ws import gps_from_thread
    
    gps_dict = {
        "DeviceID": "TRUCK-001",
        "Latitude": 10.9878,
        "Longitude": -74.7889,
        ...
    }
    
    gps_from_thread(gps_dict)  # Thread-safe broadcast

Created: 2025-10-27
"""

from typing import Dict, Any
from .wsBase import WebSocketManager
from fastapi import WebSocket


class GpsWebSocketManager(WebSocketManager):
    """
    Specialized WebSocket manager for GPS connections.
    
    Extends WebSocketManager with:
    - has_clients property to check if clients are connected
    - Conditional sending from threads based on connected clients
    - Message handling for future client commands
    """

    @property
    def has_clients(self) -> bool:
        """
        Returns True if at least one GPS client is connected.
        
        Used by broadcasters to avoid sending data when no clients exist.
        """
        return len(self.clients) > 0

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming messages from GPS WebSocket clients.
        
        Currently logs received messages. Can be extended for:
        - Update frequency control
        - Device filtering preferences
        - Map zoom/pan synchronization
        - Historical playback controls
        
        Args:
            ws: WebSocket connection that sent the message
            message: Text message received from client
        """
        print(f"[GPS-WS] Received message: {message}")
        # Future: handle commands, update frequency, client preferences, etc.


# ==========================================================
# Global Singleton Instance
# ==========================================================

# Dedicated GPS WebSocket manager instance
gps_ws_manager = GpsWebSocketManager()


# ==========================================================
# Thread-Safe Public API
# ==========================================================

def gps_from_thread(data: Dict[str, Any]):
    """
    Thread-safe entry point to broadcast GPS data to all connected clients.
    
    This function can be safely called from any thread (UDP receiver,
    background tasks, etc.) and will properly schedule the broadcast
    on the main FastAPI event loop.
    
    Args:
        data: GPS data dictionary (serialized from GPS_data model)
            {
                "DeviceID": "TRUCK-001",
                "Latitude": 10.9878,
                "Longitude": -74.7889,
                "Altitude": 50.0,
                "Accuracy": 5.0,
                "Timestamp": "2025-10-27T06:59:20Z",
                "geofence": {
                    "id": "warehouse-001",
                    "name": "Main Warehouse",
                    "event": "entry"
                }
            }
    
    Returns:
        None
    
    Example:
        from src.Core.gps_ws import gps_from_thread
        
        gps_dict = serialize_gps_row(gps_record)
        gps_from_thread(gps_dict)  # Broadcasts to all GPS WebSocket clients
    
    Performance:
        - Only sends if clients are connected (avoids unnecessary work)
        - Uses asyncio.call_soon_threadsafe for thread safety
        - Non-blocking (returns immediately)
    """
    if gps_ws_manager.has_clients:
        gps_ws_manager.send_from_thread(data)
    else:
        # Uncomment for debugging:
        # print("[GPS-WS] No clients connected. Data not sent.")
        pass