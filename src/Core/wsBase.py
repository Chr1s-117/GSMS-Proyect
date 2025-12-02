"""
WebSocket Base Manager Module
==============================

This module provides a robust, thread-safe foundation for WebSocket connection
management in the GPS tracking application. It implements best practices for
handling multiple concurrent WebSocket connections with automatic cleanup and
thread-safe broadcasting capabilities.

Architecture:
------------
- Thread-Safe Operations: All client list modifications protected by locks
- Lifecycle Management: Automatic registration, cleanup on disconnect
- Broadcasting: Efficient message distribution to all connected clients
- Event Loop Integration: Seamless communication between async and sync contexts
- Extensible Design: Base class for specialized WebSocket managers

Key Features:
-------------
1. **Thread Safety**: Lock-protected client list prevents race conditions
2. **Graceful Degradation**: Failed connections are automatically removed
3. **Cross-Thread Communication**: send_from_thread() enables background threads
   to broadcast to WebSocket clients
4. **Keep-Alive Support**: Optional connection maintenance mechanism
5. **Clean Lifecycle**: Proper handshake and cleanup on connect/disconnect

Design Patterns:
---------------
- Manager Pattern: Centralized connection management
- Template Method: handle_message() designed for subclass override
- Singleton-like Usage: Typically instantiated once per WebSocket endpoint type

Thread Safety Considerations:
----------------------------
The WebSocket manager must handle concurrent access from multiple sources:
- FastAPI async handlers (WebSocket accept/send)
- Background threads (UDP server, cache cleanup)
- Multiple concurrent WebSocket connections

All client list operations are protected by threading.Lock to prevent
race conditions and ensure consistency.

Usage Example:
-------------
    # Subclass for specific functionality
    class CustomWebSocketManager(WebSocketManager):
        async def handle_message(self, ws: WebSocket, message: str):
            data = json.loads(message)
            # Process incoming message
            await self.broadcast({"response": "processed"})
    
    # Initialize manager
    manager = CustomWebSocketManager()
    manager.set_main_loop(asyncio.get_running_loop())
    
    # Register client
    @app.websocket("/custom")
    async def websocket_endpoint(ws: WebSocket):
        await manager.register(ws)
        try:
            while True:
                message = await ws.receive_text()
                await manager.handle_message(ws, message)
        finally:
            manager.unregister(ws)
    
    # Broadcast from background thread
    def background_task():
        manager.send_from_thread({"event": "update"})

Performance Notes:
-----------------
- Lock contention is minimized by keeping critical sections small
- Client list is copied before iteration to avoid holding lock during I/O
- Failed connections are batched for removal to reduce lock acquisitions
- has_clients property enables early-exit optimization

Error Handling:
--------------
- Connection failures during accept() trigger automatic cleanup
- Send failures mark connections for removal
- Unregister operations are idempotent (safe to call multiple times)
"""

from fastapi import WebSocket
import asyncio
from typing import List, Optional, Dict, Any
import json
import threading


class WebSocketManager:
    """
    Base WebSocket manager for handling multiple concurrent client connections.
    
    This class provides thread-safe connection management with automatic cleanup,
    broadcasting capabilities, and integration with FastAPI's async event loop.
    Designed to be subclassed for specific WebSocket endpoint implementations.
    
    Attributes:
        clients (List[WebSocket]): Currently active WebSocket connections
        main_loop (Optional[asyncio.AbstractEventLoop]): FastAPI's main event loop
        _lock (threading.Lock): Thread synchronization primitive for client list
    
    Thread Safety:
        All public methods that access or modify self.clients are protected by
        self._lock, ensuring safe concurrent access from multiple threads.
    
    Lifecycle:
        1. Instantiate manager
        2. Call set_main_loop() during application startup
        3. Call register() when client connects
        4. Call broadcast() to send messages
        5. Call unregister() when client disconnects (automatic on error)
    """
    
    def __init__(self):
        """
        Initialize a new WebSocket manager instance.
        
        Sets up an empty client list, prepares event loop reference,
        and creates a thread lock for synchronization.
        """
        self.clients: List[WebSocket] = []
        """List of currently active WebSocket client connections."""
        
        self.main_loop: Optional[asyncio.AbstractEventLoop] = None
        """Reference to FastAPI's main async event loop for thread-safe scheduling."""
        
        self._lock = threading.Lock()
        """Thread lock protecting access to self.clients across concurrent operations."""
    
    def set_main_loop(self, loop: asyncio.AbstractEventLoop):
        """
        Register FastAPI's main event loop for thread-safe async operations.
        
        This method must be called during application startup (typically in the
        lifespan context manager) to enable send_from_thread() functionality.
        
        Args:
            loop: The asyncio event loop from asyncio.get_running_loop()
        
        Usage:
            @asynccontextmanager
            async def lifespan(app: FastAPI):
                loop = asyncio.get_running_loop()
                ws_manager.set_main_loop(loop)
                yield
        
        Importance:
            Without this, background threads cannot safely schedule coroutines
            on the main event loop, breaking send_from_thread() functionality.
        """
        self.main_loop = loop
    
    async def register(self, ws: WebSocket):
        """
        Accept and register a new WebSocket client connection.
        
        This method performs the WebSocket handshake and adds the client to the
        active connections list. The client is added BEFORE accept() to avoid
        race conditions where messages might be lost during registration.
        
        Args:
            ws: The WebSocket connection to register
        
        Raises:
            Exception: If WebSocket handshake fails (client is auto-unregistered)
        
        Process:
            1. Add client to list (under lock)
            2. Perform WebSocket handshake
            3. Log successful registration
            4. On failure: automatically cleanup and re-raise exception
        
        Thread Safety:
            Uses self._lock to prevent concurrent modifications to client list.
        
        Note:
            If accept() fails, unregister() is automatically called to ensure
            the failed connection is removed from the client list.
        """
        with self._lock:
            if ws not in self.clients:
                self.clients.append(ws)
        
        try:
            await ws.accept()
            print(f"[WSBase] Client registered. Total clients: {len(self.clients)}")
        except Exception:
            # Handshake failed - ensure cleanup before propagating error
            self.unregister(ws)
            raise
    
    def unregister(self, ws: WebSocket):
        """
        Remove a WebSocket client from the active connections list.
        
        This method is idempotent - calling it multiple times with the same
        WebSocket is safe and will not raise errors.
        
        Args:
            ws: The WebSocket connection to unregister
        
        Behavior:
            - If client exists in list: removes it and logs
            - If client not in list: silently succeeds (idempotent)
        
        Thread Safety:
            Uses self._lock to prevent concurrent modifications to client list.
        
        Called By:
            - Connection error handlers
            - Explicit disconnect handlers
            - Failed registration attempts
            - broadcast() when detecting dead connections
        
        Note:
            This method does NOT close the WebSocket connection - it only removes
            it from the manager's tracking. The WebSocket should be closed by
            the calling code if needed.
        """
        with self._lock:
            if ws in self.clients:
                self.clients.remove(ws)
                print(f"[WSBase] Client unregistered. Total clients: {len(self.clients)}")
    
    @property
    def has_clients(self) -> bool:
        """
        Check if any clients are currently connected.
        
        This property enables efficient early-exit logic when broadcasting.
        If no clients are connected, expensive message preparation can be skipped.
        
        Returns:
            bool: True if at least one client is connected, False otherwise
        
        Thread Safety:
            Uses self._lock to safely read client list length.
        
        Caveat:
            This only checks if the client list is non-empty, not if connections
            are actually alive. Dead connections are only detected during send
            attempts or explicit keep-alive checks.
        
        Usage:
            if ws_manager.has_clients:
                # Generate expensive data only when needed
                data = compute_expensive_statistics()
                await ws_manager.broadcast(data)
        """
        with self._lock:
            return len(self.clients) > 0
    
    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected WebSocket clients.
        
        This method attempts to send the message to every client in the list.
        Clients that fail during transmission are automatically unregistered
        and removed from the active connections.
        
        Args:
            message: Dictionary to be JSON-serialized and sent to clients
        
        Behavior:
            1. Create copy of client list (avoid holding lock during I/O)
            2. Attempt to send message to each client
            3. Track failed clients
            4. Unregister all failed clients
        
        Error Handling:
            - Failed sends: Client is marked for removal
            - Exceptions are caught and handled gracefully
            - Other clients continue to receive messages
        
        Thread Safety:
            Creates a snapshot of the client list under lock, then releases
            the lock before performing I/O operations to minimize contention.
        
        Performance:
            Batch unregistration of failed clients reduces lock acquisitions.
        
        Example:
            await manager.broadcast({
                "type": "update",
                "data": {"temperature": 25.3},
                "timestamp": "2025-12-01T10:30:00Z"
            })
        """
        to_remove = []
        
        # Create snapshot of current clients under lock
        with self._lock:
            current_clients = list(self.clients)
        
        # Attempt to send to each client (without holding lock)
        for ws in current_clients:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                # Mark failed client for removal
                to_remove.append(ws)
        
        # Batch unregister failed clients
        for ws in to_remove:
            self.unregister(ws)
    
    def send_from_thread(self, message: Dict[str, Any]):
        """
        Thread-safe method for broadcasting messages from non-async contexts.
        
        This method enables background threads (UDP server, cache cleanup, etc.)
        to safely send WebSocket messages by scheduling the broadcast coroutine
        on the main FastAPI event loop.
        
        Args:
            message: Dictionary to be JSON-serialized and sent to clients
        
        Requirements:
            - set_main_loop() must have been called during startup
            - Main event loop must be running
        
        Behavior:
            - If clients connected: schedules broadcast on main loop
            - If no clients: logs message and returns immediately
            - If main_loop not set: fails silently (should not happen in production)
        
        Thread Safety:
            Uses asyncio.run_coroutine_threadsafe() to safely schedule async
            work on the main event loop from any thread.
        
        Performance:
            Early-exit check (has_clients) prevents unnecessary scheduling overhead
            when no clients are listening.
        
        Usage Example:
            # From UDP server thread
            def handle_gps_packet(data):
                ws_manager.send_from_thread({
                    "type": "gps_update",
                    "device_id": data["imei"],
                    "location": data["coords"]
                })
            
            # From background cleanup thread
            def cleanup_task():
                ws_manager.send_from_thread({
                    "type": "maintenance",
                    "message": "Cache cleanup completed"
                })
        
        Note:
            The coroutine is scheduled as "fire and forget" - there's no
            mechanism to await its completion from the calling thread.
        """
        if not self.has_clients:
            print(f"[WSBase] No clients connected. Message not sent: {message}")
            return
        
        if self.main_loop:
            asyncio.run_coroutine_threadsafe(
                self.broadcast(message), self.main_loop
            )
    
    async def keep_alive(self, ws: WebSocket, interval: int = 60):
        """
        Optional keep-alive mechanism to maintain WebSocket connection health.
        
        This method can be used to detect dead connections by sending periodic
        ping frames or heartbeat messages. Currently it's a placeholder that
        can be extended with actual ping/pong implementation.
        
        Args:
            ws: The WebSocket connection to maintain
            interval: Time between keep-alive checks (seconds)
        
        Usage:
            @app.websocket("/endpoint")
            async def websocket_endpoint(ws: WebSocket):
                await manager.register(ws)
                
                # Start keep-alive in background
                asyncio.create_task(manager.keep_alive(ws, interval=30))
                
                try:
                    while True:
                        message = await ws.receive_text()
                        await manager.handle_message(ws, message)
                except:
                    manager.unregister(ws)
        
        Future Enhancement:
            # Send WebSocket ping frame
            await ws.send_text(json.dumps({"type": "ping"}))
            
            # Or use native WebSocket ping
            await ws.ping()
        
        Error Handling:
            If an exception occurs (connection dead), the client is automatically
            unregistered and the keep-alive loop terminates.
        
        Note:
            This is an optional feature. Basic connection management works
            without it, but keep-alive can help detect dead connections faster.
        """
        try:
            while True:
                await asyncio.sleep(interval)
                # Future improvement: implement actual ping/pong
                # await ws.ping()
        except Exception:
            # Connection is dead - cleanup
            self.unregister(ws)
    
    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming messages from WebSocket clients.
        
        This is a template method designed to be overridden by subclasses
        to implement specific message handling logic. The default implementation
        simply logs received messages.
        
        Args:
            ws: The WebSocket connection that sent the message
            message: The raw message string received from the client
        
        Subclass Implementation:
            class CustomWebSocketManager(WebSocketManager):
                async def handle_message(self, ws: WebSocket, message: str):
                    try:
                        data = json.loads(message)
                        
                        if data["type"] == "subscribe":
                            # Handle subscription
                            pass
                        elif data["type"] == "command":
                            # Execute command
                            pass
                    except json.JSONDecodeError:
                        await ws.send_text(json.dumps({
                            "error": "Invalid JSON"
                        }))
        
        Common Use Cases:
            - Client commands: Filter preferences, update frequency
            - Subscriptions: Device-specific or location-based updates
            - Bidirectional RPC: Request/response patterns
            - Authentication: Token validation, session management
        
        Note:
            This method is called automatically when a message is received
            in the WebSocket endpoint handler's message loop.
        """
        print(f"[WSBase] Received message from client: {message}")
        # Subclasses should override this method with actual logic