"""
Log WebSocket Management Module
================================

This module provides real-time log streaming capabilities via WebSocket
connections. It enables system logs, errors, and warnings to be broadcast
to connected clients in real-time, facilitating live monitoring and debugging.

Architecture:
------------
- Thread-Safe Broadcasting: Logs can be sent from any thread (UDP, HTTP, background)
- Multiple Clients: Supports multiple concurrent WebSocket connections
- Message Types: Supports different log levels (log, error, warning)
- Efficient: Only broadcasts when clients are connected

Use Cases:
---------
- Live system monitoring dashboards
- Real-time debugging and troubleshooting
- Operations monitoring and alerting
- Development and testing feedback

Message Format:
--------------
All messages are JSON objects with the following structure:
    {
        "msg_type": "log" | "error" | "warning",
        "message": "The log message content",
        "timestamp": "2025-12-01T10:30:00Z"  // Added by WebSocketManager
    }

Usage Example:
-------------
    from src.Core.log_ws import log_from_thread
    
    # From any thread or context
    log_from_thread("UDP server started successfully", "log")
    log_from_thread("Failed to process GPS packet", "error")
    log_from_thread("Cache size approaching limit", "warning")
    
    # From async context
    await log_ws_manager.broadcast({
        "msg_type": "log",
        "message": "Database migration completed"
    })

Frontend Connection:
-------------------
    const ws = new WebSocket('ws://localhost:8000/logs');
    
    ws.onmessage = (event) => {
        const log = JSON.parse(event.data);
        console.log(`[${log.msg_type}] ${log.message}`);
        
        // Display in UI based on type
        if (log.msg_type === 'error') {
            showErrorNotification(log.message);
        }
    };

Thread Safety:
-------------
The log_from_thread() function is specifically designed for thread-safe
operation, allowing background threads (UDP server, cache cleanup) to
safely broadcast logs without blocking or causing race conditions.
"""

from typing import Dict, Any
from fastapi import WebSocket
from src.DB.session import SessionLocal
from .wsBase import WebSocketManager
import json


def log_from_thread(message: str, msg_type: str = "log"):
    """
    Thread-safe entry point for broadcasting log messages to all connected clients.
    
    This function provides a simple interface for any thread or context to send
    log messages to all connected WebSocket clients. It handles the thread-safety
    concerns internally, making it safe to call from background threads.
    
    Args:
        message: The log message content to broadcast
        msg_type: Message severity level, one of:
            - "log": Informational messages (default)
            - "error": Error conditions requiring attention
            - "warning": Warning messages about potential issues
    
    Behavior:
        - If clients are connected: Message is queued for broadcast
        - If no clients connected: Message is logged to console only
    
    Examples:
        # Informational logging
        log_from_thread("Device 12345 connected successfully")
        
        # Error logging
        log_from_thread("Failed to parse GPS packet", "error")
        
        # Warning logging
        log_from_thread("Cache hit ratio below 50%", "warning")
    
    Thread Safety:
        This function uses the WebSocketManager's send_from_thread() method,
        which safely schedules the broadcast on the main event loop regardless
        of which thread calls this function.
    
    Performance:
        When no clients are connected, this function returns immediately
        without any WebSocket overhead, making it safe to call frequently.
    """
    if log_ws_manager.has_clients:
        payload: Dict[str, Any] = {"msg_type": msg_type, "message": str(message)}
        log_ws_manager.send_from_thread(payload)
    else:
        # Fallback: log to console when no WebSocket clients are listening
        print(f"[LOG-BROADCAST] No log clients connected. Message: {message}")


class LogWebSocketManager(WebSocketManager):
    """
    Specialized WebSocket manager for real-time log streaming.
    
    This class extends the base WebSocketManager with functionality specific
    to log broadcasting. It manages multiple client connections and handles
    bidirectional communication for log monitoring.
    
    Features:
        - Client presence detection (has_clients property)
        - Thread-safe message broadcasting
        - Automatic client lifecycle management
        - Support for multiple concurrent monitoring clients
    
    Attributes:
        clients: Set of active WebSocket connections (inherited)
        main_loop: Event loop for async operations (inherited)
    
    Methods:
        has_clients: Property to check if any clients are connected
        handle_message: Process incoming messages from clients (future extensibility)
    """
    
    @property
    def has_clients(self) -> bool:
        """
        Check if any log monitoring clients are currently connected.
        
        This property enables efficient early-exit logic when broadcasting logs.
        If no clients are connected, log generation overhead can be skipped.
        
        Returns:
            bool: True if at least one client is connected, False otherwise
        
        Usage:
            if log_ws_manager.has_clients:
                # Generate and send expensive log data
                log_from_thread(generate_detailed_report())
            else:
                # Skip expensive operations when no one is listening
                pass
        """
        return len(self.clients) > 0
    
    async def handle_message(self, ws: WebSocket, message: str):
        """
        Handle incoming messages from connected WebSocket clients.
        
        Currently this method logs received messages for debugging purposes.
        In future implementations, this can be extended to support:
        - Client commands (e.g., "filter by error level")
        - Log level filtering preferences
        - Client-specific configuration
        - Interactive debugging commands
        
        Args:
            ws: The WebSocket connection that sent the message
            message: The raw message string received from the client
        
        Future Enhancements:
            # Example: Client requests to filter log levels
            if message == "filter:error":
                # Only send error messages to this client
                
            # Example: Client requests historical logs
            if message.startswith("history:"):
                count = int(message.split(":")[1])
                # Send last N log messages
        
        Note:
            This is called automatically by the WebSocketManager when a client
            sends a message. Currently informational only.
        """
        print(f"[LOG-WS] Received message from client: {message}")
        # Future implementation: Parse and handle client commands
        # Examples:
        # - "filter:error" - Only receive error-level logs
        # - "mute:warning" - Don't receive warning-level logs
        # - "history:50" - Request last 50 log messages
        # - "ping" - Keepalive mechanism


# ============================================================
# GLOBAL LOG WEBSOCKET MANAGER INSTANCE
# ============================================================
log_ws_manager = LogWebSocketManager()
"""
Global singleton instance for log WebSocket management.

This instance is used throughout the application to broadcast logs to
connected monitoring clients. It should not be instantiated multiple times.

Usage:
    from src.Core.log_ws import log_ws_manager
    
    # Check for connected clients
    if log_ws_manager.has_clients:
        # Broadcast custom message
        await log_ws_manager.broadcast({"msg_type": "log", "message": "..."})

Thread Safety:
    Access to this instance is thread-safe through the provided
    log_from_thread() function.
"""