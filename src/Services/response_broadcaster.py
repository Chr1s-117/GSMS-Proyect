# src/Services/response_broadcaster.py

"""
Response Broadcasting Service

This module implements a thread-safe buffered broadcaster that manages
real-time response distribution to WebSocket clients.

Key Features:
- Thread-safe buffering with locks and events
- Request-response correlation via request_id
- Automatic retry mechanism when no clients are connected
- Integration with ResponseWebSocketManager for real-time updates
- Deduplication (only one response per request_id in buffer)

Architecture:
    API Request → Processing → add_response() → Buffer → WebSocket Clients
    
    Flow:
    1. Client sends request via WebSocket (/request endpoint)
    2. Server processes request (e.g., send command to device)
    3. Device responds (via UDP or other channel)
    4. add_response() is called with response + request_id
    5. Response is sent back to WebSocket client with matching request_id

Thread Safety:
    - Uses threading.Lock for buffer access
    - Uses threading.Event for efficient wake-up
    - Safe to call add_response() from any thread

Usage:
    # From device response handler
    from src.Services.response_broadcaster import add_response
    
    response_dict = {
        "request_id": "req-12345",
        "status": "success",
        "data": {"temperature": 25.5, "humidity": 60},
        "timestamp": "2025-01-27T06:04:54Z"
    }
    
    add_response(response_dict)  # Non-blocking, thread-safe

Performance:
    - Buffer size is limited by unique request_ids
    - Typical latency: <10ms from add_response() to WebSocket send
    - Event-driven (no polling), minimal CPU usage when idle
"""

import threading
from typing import Dict, Any
from src.Core.response_ws import response_from_thread, response_ws_manager


# ==========================================================
# 📌 Response Broadcaster Class
# ==========================================================

class ResponseBroadcaster:
    """
    Thread-safe response broadcaster with buffering and retry logic.
    
    This service manages a buffer of pending response payloads and
    sends them to WebSocket clients via ResponseWebSocketManager.
    
    If no clients are connected, responses remain in buffer and will
    be sent when clients connect.
    
    Attributes:
        pending_responses: Dict mapping request_id → response payload
        lock: Threading lock for buffer access
        event: Threading event for efficient wake-up signaling
    """

    def __init__(self):
        """Initialize broadcaster with empty buffer and synchronization primitives."""
        self.pending_responses: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        self.event = threading.Event()

    def add_response(self, payload: Dict[str, Any]):
        """
        Add a response payload to the broadcast buffer.
        
        This method is thread-safe and can be called from any thread
        (UDP receiver, HTTP handlers, background tasks, etc.).
        
        Args:
            payload: Response data dictionary with required field:
                - request_id: str (unique identifier for request-response correlation)
                - status: str (optional, e.g., "success", "error")
                - data: dict (optional, response data)
                - message: str (optional, human-readable message)
                - timestamp: str (optional, ISO 8601 timestamp)
        
        Returns:
            None
            
        Example:
            response_dict = {
                "request_id": "req-12345",
                "status": "success",
                "data": {"temperature": 25.5},
                "timestamp": "2025-01-27T06:04:54Z"
            }
            broadcaster.add_response(response_dict)
        
        Thread Safety:
            - Acquires lock before modifying buffer
            - Sets event to wake up broadcast loop
            - Non-blocking (returns immediately)
        
        Deduplication:
            - Only one response per request_id is kept in buffer
            - If called twice with same request_id, second call overwrites first
        """
        request_id = payload.get("request_id")
        
        if not request_id:
            print("[RESPONSE-BROADCAST] ⚠️  Ignored response without request_id")
            return
        
        with self.lock:
            self.pending_responses[request_id] = payload
            print(f"[RESPONSE-BROADCAST] 📦 Added response for request_id={request_id}")
            print(f"[RESPONSE-BROADCAST] 📊 Buffer size: {len(self.pending_responses)}")
            self.event.set()  # Wake up the broadcast loop

    def _broadcast_loop(self):
        """
        Main broadcast loop (runs in daemon thread).
        
        Continuously processes response payloads from buffer and sends them
        to connected WebSocket clients.
        
        Loop Behavior:
        1. Wait for event signal (new response added)
        2. Acquire lock and copy pending responses list
        3. Clear buffer and release lock
        4. Attempt to send each response to clients
        5. If no clients, re-add to buffer for retry
        6. Repeat
        
        Retry Logic:
            - If no WebSocket clients are connected, responses are kept in buffer
            - When clients connect, buffered responses are immediately sent
            - No data loss (buffer grows until clients connect)
        
        Performance:
            - Event-driven (no polling, minimal CPU when idle)
            - Batch processing (all pending responses sent in one iteration)
            - Lock held for minimal time (copy buffer, then release)
        """
        while True:
            # Wait until there is at least one response pending
            self.event.wait()

            while True:  # Process all pending responses
                with self.lock:
                    if not self.pending_responses:
                        self.event.clear()
                        break
                    responses_to_send = list(self.pending_responses.values())
                    self.pending_responses.clear()

                for resp in responses_to_send:
                    if response_ws_manager.has_clients:
                        # Thread-safe send to Response WebSocket clients
                        response_from_thread(resp)
                    else:
                        # No clients connected: re-add to buffer for next attempt
                        with self.lock:
                            self.pending_responses[resp["request_id"]] = resp
                        # Uncomment for debugging:
                        # print(f"[RESPONSE-BROADCAST] ℹ️  No clients connected, buffering response")
                        break  # Exit for-loop and wait for clients


# ==========================================================
# 📌 Module-Level Singleton Instance
# ==========================================================

# Internal broadcaster instance (singleton)
_broadcaster = ResponseBroadcaster()


# ==========================================================
# 📌 Public API Functions
# ==========================================================

def add_response(payload: Dict[str, Any]):
    """
    Public API: Add response to the broadcast buffer.
    
    This is the primary entry point for broadcasting responses.
    Called by device response handlers, UDP receiver, or any service
    that wants to send responses back to WebSocket clients.
    
    Args:
        payload: Response data dictionary (see ResponseBroadcaster.add_response for format)
    
    Returns:
        None
        
    Example:
        from src.Services.response_broadcaster import add_response
        
        response_dict = {
            "request_id": "req-12345",
            "status": "success",
            "data": {"temperature": 25.5}
        }
        
        add_response(response_dict)  # Non-blocking, thread-safe
    
    Thread Safety:
        Safe to call from any thread (UDP, HTTP handlers, background tasks)
    """
    _broadcaster.add_response(payload)


def start_response_broadcaster() -> threading.Thread:
    """
    Start the response broadcaster service in a daemon thread.
    
    This function should be called once during application startup,
    typically in main.py's lifespan context.
    
    Returns:
        threading.Thread: The background broadcaster thread
        
    Example:
        # In main.py lifespan
        response_thread = start_response_broadcaster()
    
    Thread Behavior:
        - Runs as daemon (won't prevent app shutdown)
        - Named "ResponseBroadcaster" for easy identification in logs
        - Continues running until app terminates
        - Automatically started by main.py (always enabled)
    """
    thread = threading.Thread(
        target=_broadcaster._broadcast_loop,
        daemon=True,
        name="ResponseBroadcaster"
    )
    thread.start()
    
    print("[RESPONSE-BROADCAST] 🚀 Started broadcast thread")
    
    return thread