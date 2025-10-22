# src/Services/gps_broadcaster.py

"""
GPS Broadcasting Service

This service manages a buffer of pending GPS data payloads and
broadcasts them to all connected GPS WebSocket clients using
thread-safe communication.

Architecture:
- Maintains a FIFO buffer of GPS payloads
- Broadcast loop runs in daemon thread
- Thread-safe operations using Lock
- Automatic retry if no clients connected
- Integrates with GPSWebSocketManager

Use Cases:
- Real-time GPS updates to frontend map
- Multi-client GPS data distribution
- Buffering when no clients connected
"""

import threading
from typing import Dict, Any, List
from src.Core.gps_ws import gps_ws_manager, gps_from_thread
from src.Core.log_ws import log_ws_manager, log_from_thread


class GPSBroadcaster:
    """
    Service that manages a buffer of pending GPS data
    and sends them via GPSWebSocketManager using the thread-safe entry point.
    
    Features:
    - FIFO buffer for GPS payloads
    - Event-driven broadcast loop (efficient CPU usage)
    - Thread-safe operations
    - Automatic retry when no clients connected
    - Logging integration
    
    Thread Safety:
    All operations on pending_gps list are protected by self.lock
    """

    def __init__(self):
        """Initialize broadcaster with empty buffer and synchronization primitives."""
        self.pending_gps: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self.event = threading.Event()
        print("[GPS-BROADCAST] ✅ Initialized")

    def add_gps(self, payload: Dict[str, Any]):
        """
        Add a GPS data payload to the buffer and notify the broadcast loop.
        
        Args:
            payload: Dictionary with GPS fields (already serialized):
                {
                    "DeviceID": "TRUCK-001",
                    "Latitude": 10.9878,
                    "Longitude": -74.7889,
                    "Altitude": 12.5,
                    "Accuracy": 8.0,
                    "Timestamp": "2025-10-22T09:34:28Z",
                    "geofence": {
                        "id": "warehouse-001",
                        "name": "Main Warehouse",
                        "event": "entry"
                    }
                }
        
        Example:
            from src.Services.gps_broadcaster import add_gps
            
            add_gps({
                "DeviceID": "TRUCK-001",
                "Latitude": 10.9878,
                "Longitude": -74.7889,
                ...
            })
        """
        if not payload:
            print("[GPS-BROADCAST] ⚠️ Ignored empty GPS payload")
            return

        with self.lock:
            self.pending_gps.append(payload)
            count = len(self.pending_gps)
            self.event.set()  # Wake up the broadcast loop
            
            # Only log if buffer is getting large (avoid spam)
            if count > 10:
                print(f"[GPS-BROADCAST] ⚠️ Buffer growing: {count} pending GPS payloads")

    def _broadcast_loop(self):
        """
        Continuously tries to send pending GPS data if clients are connected.
        
        This runs in a daemon thread and:
        1. Waits for event signal (efficient - no busy waiting)
        2. Processes all pending GPS payloads
        3. Sends to all connected GPS WebSocket clients
        4. Re-buffers if no clients available
        5. Logs to connected log clients
        
        Performance:
        - Event-driven (no CPU waste)
        - Batch processing (processes all pending at once)
        - Thread-safe (uses lock for buffer access)
        """
        print("[GPS-BROADCAST] 🔄 Broadcast loop started")
        
        while True:
            # Wait until there is at least one GPS payload pending
            self.event.wait()

            while True:  # Process all pending GPS payloads
                with self.lock:
                    if not self.pending_gps:
                        self.event.clear()
                        break
                    
                    # Take snapshot of pending GPS
                    gps_to_send = list(self.pending_gps)
                    self.pending_gps.clear()

                # Send outside of lock to avoid blocking
                for gps_data in gps_to_send:
                    if gps_ws_manager.has_clients:
                        # Thread-safe send to GPS clients
                        gps_from_thread(gps_data)

                        # Log only if log clients are connected (avoid spam)
                        if log_ws_manager.has_clients:
                            device_id = gps_data.get("DeviceID", "unknown")
                            log_from_thread(
                                f"[GPS-BROADCAST] Sent GPS for device {device_id}",
                                msg_type="log"
                            )
                    else:
                        # No clients: re-add to buffer for next attempt
                        with self.lock:
                            self.pending_gps.append(gps_data)
                        print("[GPS-BROADCAST] ⏳ No clients connected, buffering GPS data")
                        break  # Exit for-loop and retry later


# ==========================================================
# Internal broadcaster instance
# ==========================================================
_broadcaster = GPSBroadcaster()


# ==========================================================
# Public API
# ==========================================================

def add_gps(payload: Dict[str, Any]):
    """
    Public function to add GPS data to broadcast buffer.
    
    This is the main entry point used by other services
    (UDP, request handlers, etc.) to broadcast GPS data.
    
    Args:
        payload: GPS data dictionary (already serialized)
    
    Example:
        from src.Services.gps_broadcaster import add_gps
        
        add_gps({
            "DeviceID": "TRUCK-001",
            "Latitude": 10.9878,
            "Longitude": -74.7889,
            "Altitude": 12.5,
            "Accuracy": 8.0,
            "Timestamp": "2025-10-22T09:34:28Z",
            "geofence": {"id": "warehouse-001", "name": "Main Warehouse", "event": "entry"}
        })
    """
    _broadcaster.add_gps(payload)


def start_gps_broadcaster() -> threading.Thread:
    """
    Start the GPS broadcast loop in a daemon thread.
    
    This should be called once during application startup (in main.py lifespan).
    
    Returns:
        Thread object for the broadcast loop
    
    Example:
        # In main.py lifespan
        from src.Services.gps_broadcaster import start_gps_broadcaster
        
        start_gps_broadcaster()
    """
    thread = threading.Thread(
        target=_broadcaster._broadcast_loop,
        daemon=True,
        name="GPSBroadcaster"
    )
    thread.start()
    print("[GPS-BROADCAST] ✅ Broadcast thread started")
    return thread