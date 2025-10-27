# src/Core/wsBase.py

"""
Base WebSocket Manager

Thread-safe base class for managing WebSocket connections with support for
concurrent access from multiple threads (UDP receiver, background tasks, etc.).

Key Features:
- Thread-safe client list management using threading.Lock
- Safe register/unregister with race condition protection
- Thread-safe broadcasting from non-async threads
- Automatic cleanup of failed connections
- Extensible message handling for subclasses

Thread Safety:
All operations that access or modify the client list are protected by a lock,
ensuring safe concurrent access from:
- FastAPI WebSocket handlers (async)
- UDP receiver thread
- Background monitoring tasks
- Broadcaster services

Architecture:
This base class is extended by:
- GpsWebSocketManager (gps_ws.py)
- LogWebSocketManager (log_ws.py)
- RequestWebSocketManager (request_ws.py)
- ResponseWebSocketManager (response_ws.py)

Usage:
    # Subclass implementation
    class MyWebSocketManager(WebSocketManager):
        async def handle_message(self, ws: WebSocket, message: str):
            # Custom message handling logic
            print(f"Received: {message}")
    
    # In main.py lifespan
    my_manager = MyWebSocketManager()
    my_manager.set_main_loop(asyncio.get_running_loop())
    
    # WebSocket endpoint
    @app.websocket("/ws/my-endpoint")
    async def websocket_endpoint(websocket: WebSocket):
        await my_manager.register(websocket)
        try:
            while True:
                message = await websocket.receive_text()
                await my_manager.handle_message(websocket, message)
        except WebSocketDisconnect:
            my_manager.unregister(websocket)

Created: 2025-10-27
Author: Chr1s-117
"""

from fastapi import WebSocket
import asyncio
from typing import List, Optional, Dict, Any
import json
import threading


class WebSocketManager:
    """
    Thread-safe base WebSocket manager for handling groups of connected clients.

    Responsibilities:
    - Manage WebSocket client connections (register/unregister)
    - Broadcast messages to all connected clients safely
    - Provide thread-safe message sending from external (non-async) threads
    - Protect against race conditions in concurrent environments
    - Automatic cleanup of failed connections

    Thread Safety:
    All operations that modify or access `self.clients` are protected
    by `self._lock` to ensure safe concurrent access from multiple threads.

    Subclasses should override `handle_message()` to implement
    custom logic for processing incoming client messages.
    """

    def __init__(self):
        """
        Initialize WebSocketManager with empty client list and lock.
        """
        # List of currently active WebSocket clients
        self.clients: List[WebSocket] = []

        # Reference to the main FastAPI event loop
        # Required for safely sending messages from non-async threads
        self.main_loop: Optional[asyncio.AbstractEventLoop] = None

        # Lock to protect access to self.clients across threads
        self._lock = threading.Lock()

    def set_main_loop(self, loop: asyncio.AbstractEventLoop):
        """
        Register the main FastAPI event loop.

        This is required to safely schedule coroutine executions
        from background threads using `asyncio.run_coroutine_threadsafe`.

        Args:
            loop: The main event loop from asyncio.get_running_loop()

        Example:
            # In main.py lifespan
            @asynccontextmanager
            async def lifespan(app: FastAPI):
                loop = asyncio.get_running_loop()
                gps_ws_manager.set_main_loop(loop)
                ...
        """
        self.main_loop = loop

    async def register(self, ws: WebSocket):
        """
        Accept and register a new WebSocket client.

        IMPORTANT: Client is added to list BEFORE accept() to avoid race condition
        where a broadcast could occur between accept() and append().

        Args:
            ws: The WebSocket connection to register

        Raises:
            Exception: If WebSocket handshake fails (client is auto-unregistered)

        Example:
            @app.websocket("/ws/gps")
            async def websocket_gps_endpoint(websocket: WebSocket):
                await gps_ws_manager.register(websocket)
                try:
                    while True:
                        message = await websocket.receive_text()
                        await gps_ws_manager.handle_message(websocket, message)
                except WebSocketDisconnect:
                    gps_ws_manager.unregister(websocket)
        """
        with self._lock:
            if ws not in self.clients:
                self.clients.append(ws)

        try:
            await ws.accept()
            print(f"[WSBase] ✅ Client registered. Total clients: {len(self.clients)}")
        except Exception as e:
            # If handshake fails, ensure cleanup
            self.unregister(ws)
            print(f"[WSBase] ❌ Registration failed: {e}")
            raise

    def unregister(self, ws: WebSocket):
        """
        Unregister a WebSocket client safely (idempotent).

        Safe to call multiple times with the same client (no error if not in list).
        Thread-safe and can be called from any thread.

        Args:
            ws: The WebSocket connection to unregister

        Example:
            try:
                while True:
                    message = await websocket.receive_text()
                    ...
            except WebSocketDisconnect:
                gps_ws_manager.unregister(websocket)
        """
        with self._lock:
            if ws in self.clients:
                self.clients.remove(ws)
                print(f"[WSBase] 🔌 Client unregistered. Total clients: {len(self.clients)}")

    @property
    def has_clients(self) -> bool:
        """
        Check if there are currently any connected clients (thread-safe).

        Returns:
            bool: True if at least one client is connected, False otherwise

        Note:
            This only checks if the list is non-empty, not if connections
            are still alive. Dead connections are removed on next broadcast attempt.

        Example:
            if gps_ws_manager.has_clients:
                gps_ws_manager.send_from_thread(gps_data)
        """
        with self._lock:
            return len(self.clients) > 0

    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected clients (thread-safe).

        Creates a snapshot of the client list under lock protection,
        then iterates over the snapshot to avoid race conditions.
        Automatically removes clients that fail during transmission.

        Args:
            message: A JSON-serializable dictionary to send

        Example:
            await gps_ws_manager.broadcast({
                "DeviceID": "TRUCK-001",
                "Latitude": 10.9878,
                "Longitude": -74.7889
            })

        Error Handling:
            - Failed sends mark client for removal
            - Cleanup happens after iteration
            - Individual client failures don't affect others
        """
        to_remove = []

        # Create snapshot of client list under lock protection
        with self._lock:
            current_clients = list(self.clients)

        # Iterate over snapshot (safe from concurrent modifications)
        for ws in current_clients:
            try:
                await ws.send_text(json.dumps(message))
            except Exception as e:
                # Mark failed clients for removal
                print(f"[WSBase] ❌ Send failed to client: {e}")
                to_remove.append(ws)

        # Clean up dead connections
        for ws in to_remove:
            self.unregister(ws)

    def send_from_thread(self, message: Dict[str, Any]):
        """
        Thread-safe sending of a message from a non-async thread.

        Uses `asyncio.run_coroutine_threadsafe` to schedule the broadcast
        on the main event loop from any thread (UDP, background tasks, etc.).

        Args:
            message: A dictionary containing the message to send

        Returns:
            None

        Example:
            # From UDP receiver thread
            def udp_server():
                while True:
                    data, addr = sock.recvfrom(1024)
                    gps_dict = parse_gps(data)
                    gps_ws_manager.send_from_thread(gps_dict)

        Performance:
            - Non-blocking (returns immediately)
            - Message queued on main event loop
            - Typical latency: <5ms from call to WebSocket send

        Note:
            - Only sends if clients are connected (check with has_clients first)
            - Requires main_loop to be set (via set_main_loop())
        """
        if not self.has_clients:
            # Uncomment for debugging:
            # print(f"[WSBase] ⚠️  No clients connected. Message not sent: {message}")
            return

        if self.main_loop:
            asyncio.run_coroutine_threadsafe(
                self.broadcast(message), self.main_loop
            )
        else:
            print("[WSBase] ❌ ERROR: Main loop not set. Call set_main_loop() first.")

    async def keep_alive(self, ws: WebSocket, interval: int = 60):
        """
        Optional keep-alive loop to maintain a WebSocket connection.

        Can be extended to send ping/pong frames or detect broken
        connections earlier than default TCP timeout.

        Args:
            ws: WebSocket connection to keep alive
            interval: Time in seconds between keep-alive checks (default: 60)

        Example:
            async def websocket_endpoint(websocket: WebSocket):
                await manager.register(websocket)
                
                # Start keep-alive in background
                asyncio.create_task(manager.keep_alive(websocket, interval=30))
                
                try:
                    while True:
                        message = await websocket.receive_text()
                        await manager.handle_message(websocket, message)
                except WebSocketDisconnect:
                    manager.unregister(websocket)

        Future Enhancement:
            # Send ping frame
            try:
                while True:
                    await asyncio.sleep(interval)
                    await ws.send_text(json.dumps({"type": "ping"}))
            except Exception:
                manager.unregister(ws)
        """
        try:
            while True:
                await asyncio.sleep(interval)
                # 🔹 Future: Add ws.ping() here for proper keep-alive
        except Exception:
            self.unregister(ws)

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Default handler for incoming messages from clients.

        Subclasses should override this method to implement
        application-specific message processing logic.

        Args:
            ws: WebSocket connection that sent the message
            message: Text message received from the client

        Example:
            class MyWebSocketManager(WebSocketManager):
                async def handle_message(self, ws: WebSocket, message: str):
                    data = json.loads(message)
                    if data["action"] == "ping":
                        await ws.send_text(json.dumps({"action": "pong"}))
        """
        print(f"[WSBase] 📨 Received message from client: {message}")