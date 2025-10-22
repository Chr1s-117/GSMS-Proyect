# src/Core/wsBase.py

from fastapi import WebSocket
import asyncio
from typing import List, Optional, Dict, Any
import json
import threading


class WebSocketManager:
    """
    Base WebSocket manager that handles a group of connected clients.

    Responsibilities:
    - Manage WebSocket client connections (register/unregister).
    - Broadcast messages to all connected clients safely.
    - Provide thread-safe message sending from external (non-async) threads.
    - Optional keep-alive support for long-lived connections.

    Improvements:
    - Thread-safe access to client list using a Lock.
    - Register adds client before ws.accept() to avoid race gap.
    - Safer unregister (idempotent).
    - Prepared for future alive-check (ping/pong).

    Subclasses should override `handle_message()` to implement
    custom logic for processing incoming client messages.
    """

    def __init__(self):
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
        """
        self.main_loop = loop

    async def register(self, ws: WebSocket):
        """
        Accept and register a new WebSocket client.

        Args:
            ws: The WebSocket connection to register.

        Notes:
            - Client is added to the list BEFORE accepting to avoid timing gaps.
            - If handshake fails, client is automatically cleaned up.
        """
        with self._lock:
            if ws not in self.clients:
                self.clients.append(ws)

        try:
            await ws.accept()
            print(f"[WSBase] Client registered. Total clients: {len(self.clients)}")
        except Exception:
            # If handshake fails, ensure cleanup
            self.unregister(ws)
            raise

    def unregister(self, ws: WebSocket):
        """
        Unregister a WebSocket client safely (idempotent).

        Safe to call if the client disconnects or fails.
        Multiple calls with the same WebSocket are handled gracefully.
        """
        with self._lock:
            if ws in self.clients:
                self.clients.remove(ws)
                print(f"[WSBase] Client unregistered. Total clients: {len(self.clients)}")

    @property
    def has_clients(self) -> bool:
        """
        Check if there are currently any connected clients.

        Returns:
            True if at least one client is connected, False otherwise.

        Notes:
            - This only checks if the list is non-empty, not if connections are alive.
            - Thread-safe access protected by lock.
        """
        with self._lock:
            return len(self.clients) > 0

    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected clients.

        Args:
            message: A JSON-serializable dictionary to send.

        Notes:
            - Removes clients that fail during transmission.
            - Exceptions are caught individually per client.
            - Thread-safe: creates snapshot of client list before iteration.
        """
        to_remove = []
        
        # Create snapshot of clients while holding lock
        with self._lock:
            current_clients = list(self.clients)

        # Send to all clients (outside lock to avoid blocking)
        for ws in current_clients:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                # Mark failed clients for removal
                to_remove.append(ws)

        # Clean up dead connections
        for ws in to_remove:
            self.unregister(ws)

    def send_from_thread(self, message: Dict[str, Any]):
        """
        Thread-safe sending of a message from a non-async thread.

        Args:
            message: A dictionary containing the message to send.

        Notes:
            - Only sends if there is at least one connected client.
            - Uses the registered main event loop to schedule coroutine.
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
        Optional keep-alive loop to maintain a WebSocket connection.

        Args:
            ws: WebSocket connection to keep alive.
            interval: Time in seconds between keep-alive checks.

        Notes:
            - Can be extended to send ping/pong frames or detect
              broken connections earlier than default TCP timeout.
            - Future improvement: send ws.ping() here to verify connection.
        """
        try:
            while True:
                await asyncio.sleep(interval)
                # 🔹 Future improvement: send ws.ping() here
        except Exception:
            self.unregister(ws)

    async def handle_message(self, ws: WebSocket, message: str):
        """
        Default handler for incoming messages from clients.

        Subclasses should override this method to implement
        application-specific message processing logic.

        Args:
            ws: WebSocket connection that sent the message.
            message: Text message received from the client.
        """
        print(f"[WSBase] Received message from client: {message}")