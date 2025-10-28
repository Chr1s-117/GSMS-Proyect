# src/Core/wsBase.py

from fastapi import WebSocket
import asyncio
from typing import List, Optional, Dict, Any
import json
import threading


class WebSocketManager:
    """
    Base WebSocket manager that handles a group of connected clients.

    Improvements:
    - Thread-safe access to client list using a Lock.
    - Register adds client before ws.accept() to avoid race gap.
    - Safer unregister (idempotent).
    - Prepared for future alive-check (ping/pong).
    """

    def __init__(self):
        # List of currently active WebSocket clients
        self.clients: List[WebSocket] = []

        # Reference to the main FastAPI event loop
        self.main_loop: Optional[asyncio.AbstractEventLoop] = None

        # Lock to protect access to self.clients across threads
        self._lock = threading.Lock()

    def set_main_loop(self, loop: asyncio.AbstractEventLoop):
        """
        Register the main FastAPI event loop.
        """
        self.main_loop = loop

    async def register(self, ws: WebSocket):
        """
        Accept and register a new WebSocket client.
        Added to self.clients before accept() to avoid timing gaps.
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
        """
        with self._lock:
            if ws in self.clients:
                self.clients.remove(ws)
                print(f"[WSBase] Client unregistered. Total clients: {len(self.clients)}")

    @property
    def has_clients(self) -> bool:
        """
        Check if there are currently any connected clients.
        NOTE: This only checks if the list is non-empty,
        not if connections are alive.
        """
        with self._lock:
            return len(self.clients) > 0

    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected clients.
        Removes clients that fail during transmission.
        """
        to_remove = []
        with self._lock:
            current_clients = list(self.clients)

        for ws in current_clients:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                to_remove.append(ws)

        for ws in to_remove:
            self.unregister(ws)

    def send_from_thread(self, message: Dict[str, Any]):
        """
        Thread-safe sending of a message from a non-async thread.
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
        Can be extended to send ping/pong frames.
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
        Subclasses should override this method to implement logic.
        """
        print(f"[WSBase] Received message from client: {message}")
