# src/Core/wsBase.py

from fastapi import WebSocket
import asyncio
from typing import List, Optional, Dict, Any
import json


class WebSocketManager:
    """
    Base WebSocket manager that handles a group of connected clients.

    Responsibilities:
    - Manage WebSocket client connections (register/unregister).
    - Broadcast messages to all connected clients safely.
    - Provide thread-safe message sending from external (non-async) threads.
    - Optional keep-alive support for long-lived connections.

    Subclasses should override `handle_message()` to implement
    custom logic for processing incoming client messages.
    """

    def __init__(self):
        # List of currently active WebSocket clients
        self.clients: List[WebSocket] = []

        # Reference to the main FastAPI event loop
        # Required for safely sending messages from non-async threads
        self.main_loop: Optional[asyncio.AbstractEventLoop] = None

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
        """
        await ws.accept()
        self.clients.append(ws)
        print(f"[WSBase] Client registered. Total clients: {len(self.clients)}")

    def unregister(self, ws: WebSocket):
        """
        Unregister a WebSocket client.

        Safe to call if the client disconnects or fails.
        """
        if ws in self.clients:
            self.clients.remove(ws)
            print(f"[WSBase] Client unregistered. Total clients: {len(self.clients)}")

    @property
    def has_clients(self) -> bool:
        """
        Check if there are currently any connected clients.

        Returns:
            True if at least one client is connected, False otherwise.
        """
        return len(self.clients) > 0

    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected clients.

        Args:
            message: A JSON-serializable dictionary to send.

        Notes:
            - Removes clients that fail during transmission.
            - Exceptions are caught individually per client.
        """
        to_remove = []
        for ws in self.clients:
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
            Can be extended to send ping/pong frames or detect
            broken connections earlier than default TCP timeout.
        """
        try:
            while True:
                await asyncio.sleep(interval)
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