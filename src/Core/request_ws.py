# src/Core/request_ws.py

"""
Request WebSocket Manager

Manages WebSocket connections for handling client requests and coordinating responses.

This module delegates all business logic to request_handlers.py, maintaining
separation of concerns between WebSocket connection management and request processing.

Features:
- Thread-safe request handling
- Action-based routing to handlers
- Real-time GPS position monitoring
- Subscription-based data streaming
- Response broadcasting coordination

Supported Actions:
- ping: Health check
- get_devices: List all registered devices
- get_last_positions: Get latest GPS from all devices (with optional subscription)
- get_history: Get historical GPS data for time range
- get_timestamp_range: Get available data time bounds

Architecture:
    WebSocket Client → request_ws.py → request_handlers.py → Repository → Database
                                     ↓
                              response_broadcaster.py → response_ws.py → WebSocket Client

Integration:
- Receives requests from frontend via WebSocket
- Delegates to request_handlers.py for processing
- Coordinates responses via response_broadcaster.py
- Manages real-time monitoring subscriptions

Usage:
    # WebSocket endpoint in main.py
    @app.websocket("/ws/request")
    async def websocket_request_endpoint(websocket: WebSocket):
        await request_ws_manager.handle_connection(websocket)

Created: 2025-10-27
"""

from typing import Dict, Any
from fastapi import WebSocket
import asyncio
import json
from .wsBase import WebSocketManager
from src.Services.response_broadcaster import add_response
from src.Services.gps_broadcaster import add_gps
from src.DB.session import SessionLocal
from src.Repositories.gps_data import get_last_gps_all_devices
from src.Services import request_handlers as handlers


# ==========================================================
# Request WebSocket Manager Class
# ==========================================================

class RequestWebSocketManager(WebSocketManager):
    """
    Specialized WebSocket manager for handling client requests.
    
    This manager:
    1. Receives action-based requests from clients
    2. Delegates processing to request_handlers.py
    3. Manages real-time monitoring subscriptions
    4. Coordinates responses via response_broadcaster.py
    
    Monitoring:
    - Supports subscription to real-time GPS position updates
    - Single monitor for all devices (efficient)
    - Automatic cleanup on unsubscribe
    """

    def __init__(self):
        super().__init__()
        
        # Real-time monitoring task
        self._monitor_last_positions_task: asyncio.Task | None = None
        self._monitor_last_positions_active: bool = False
        
        # Cache of last known positions (for change detection)
        self._last_positions: dict = {}

    @property
    def has_clients(self) -> bool:
        """Returns True if at least one request client is connected."""
        return len(self.clients) > 0

    # ==========================================================
    # Real-Time GPS Position Monitor
    # ==========================================================

    async def _monitor_last_positions(self):
        """
        Monitor latest GPS positions for ALL active devices.
        
        This is the primary real-time GPS update mechanism.
        Runs continuously while subscribed, checking for position
        changes every 500ms.
        
        Flow:
        1. Query latest GPS for all devices
        2. Compare with cached positions
        3. Broadcast changes via gps_broadcaster
        4. Update cache
        5. Sleep 500ms
        6. Repeat
        
        Performance:
        - Single query for all devices (efficient)
        - Only broadcasts changes (reduces traffic)
        - 500ms polling interval (configurable)
        
        Cleanup:
        - Automatically stops when unsubscribed
        - Clears cache on stop
        """
        print("[REQUEST-WS] 🔄 Monitor last_positions started")
        
        while self._monitor_last_positions_active:
            try:
                with SessionLocal() as db:
                    current_positions = get_last_gps_all_devices(db)
                
                # Broadcast changed positions
                for device_id, gps_data in current_positions.items():
                    if device_id not in self._last_positions or \
                       self._last_positions[device_id] != gps_data:
                        add_gps(gps_data)
                        self._last_positions[device_id] = gps_data
                        print(f"[REQUEST-WS] 📍 Updated position for {device_id}")
                
                # Detect removed devices
                removed_devices = set(self._last_positions.keys()) - set(current_positions.keys())
                for device_id in removed_devices:
                    del self._last_positions[device_id]
                    print(f"[REQUEST-WS] 🗑️  Removed device {device_id} from cache")
            
            except Exception as e:
                print(f"[REQUEST-WS] ❌ Error in _monitor_last_positions: {e}")
            
            await asyncio.sleep(0.5)
        
        # Cleanup on stop
        self._last_positions.clear()
        print("[REQUEST-WS] ⏹️  Monitor last_positions stopped")

    # ==========================================================
    # Message Handler (Routes to request_handlers.py)
    # ==========================================================

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming WebSocket messages and route to appropriate handlers.
        
        All business logic is delegated to request_handlers.py for
        separation of concerns and easier testing.
        
        Message Format:
            {
                "action": "ping" | "get_devices" | "get_last_positions" | ...,
                "request_id": "req-12345",
                "params": {
                    "device_id": "TRUCK-001",
                    "start": "2025-10-27T00:00:00Z",
                    ...
                }
            }
        
        Response Format:
            {
                "action": "ping",
                "request_id": "req-12345",
                "status": "success" | "error",
                "data": {...}
            }
        
        Args:
            ws: WebSocket connection that sent the message
            message: JSON string with action and parameters
        """
        print(f"[REQUEST-WS] 📨 Received: {message[:100]}...")  # Truncate long messages

        # Parse JSON
        try:
            data = json.loads(message)
        except json.JSONDecodeError as e:
            print(f"[REQUEST-WS] ❌ Invalid JSON: {e}")
            return

        # Extract required fields
        action = data.get("action")
        request_id = data.get("request_id")
        params: Dict[str, Any] = data.get("params", {})

        if not action:
            print("[REQUEST-WS] ⚠️  Missing 'action' field")
            return

        print(f"[REQUEST-WS] 🎯 Action: {action}, Request ID: {request_id}")

        # ======================================================
        # Simple Actions (delegated to handlers)
        # ======================================================
        SIMPLE_ACTIONS = [
            "ping",
            "get_devices",
            "get_history",
            "get_timestamp_range"
        ]

        if action in SIMPLE_ACTIONS:
            handler_map = {
                "ping": handlers.handle_ping,
                "get_devices": handlers.handle_get_devices,
                "get_history": handlers.handle_get_history,
                "get_timestamp_range": handlers.handle_get_timestamp_range
            }
            
            response = handler_map[action](params, request_id)
            add_response(response)
            return

        # ======================================================
        # get_last_positions (with optional subscription)
        # ======================================================
        elif action == "get_last_positions":
            # Get initial positions
            response = handlers.handle_get_last_positions(params, request_id)
            add_response(response)

            # Handle subscription toggle
            subscribe = params.get("subscribe", False)
            
            if subscribe:
                # Start monitoring
                self._monitor_last_positions_active = True
                
                if not self._monitor_last_positions_task or self._monitor_last_positions_task.done():
                    self._monitor_last_positions_task = asyncio.create_task(
                        self._monitor_last_positions()
                    )
                
                print("[REQUEST-WS] ✅ Monitor last_positions ACTIVATED")
            
            else:
                # Stop monitoring
                self._monitor_last_positions_active = False
                
                if self._monitor_last_positions_task and not self._monitor_last_positions_task.done():
                    self._monitor_last_positions_task.cancel()
                    self._monitor_last_positions_task = None
                
                print("[REQUEST-WS] ❌ Monitor last_positions DEACTIVATED")

        # ======================================================
        # Unknown Action
        # ======================================================
        else:
            print(f"[REQUEST-WS] ⚠️  Unknown action: {action}")
            add_response(handlers.build_response(
                action,
                request_id,
                {"error": f"Unknown action '{action}'"},
                status="error"
            ))


# ==========================================================
# Global Singleton Instance
# ==========================================================

# Single instance for all request WebSocket connections
request_ws_manager = RequestWebSocketManager()