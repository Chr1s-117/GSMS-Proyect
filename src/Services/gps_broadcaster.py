# src/Services/gps_broadcaster.py

import threading
from typing import Dict, Any, List
from src.Core import gps_ws, log_ws


class GPSBroadcaster:
    """
    Service that manages a buffer of pending GPS data
    and sends them via GPSWebSocketManager using the thread-safe entry point.
    """

    def __init__(self):
        self.pending_gps: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self.event = threading.Event()

    def add_gps(self, payload: Dict[str, Any]):
        """
        Add a GPS data payload to the buffer and notify the broadcast loop.
        Payload must be a dict with GPS fields (e.g., lat, lon, timestamp...).
        """
        if not payload:
            print("[GPS-BROADCAST] Ignored empty GPS payload")
            return

        with self.lock:
            self.pending_gps.append(payload)
            print(f"[GPS-BROADCAST] Added GPS payload. Pending: {len(self.pending_gps)}")
            self.event.set()  # wake up the broadcast loop

    def _broadcast_loop(self):
        """
        Continuously tries to send pending GPS data if clients are connected.
        """
        while True:
            # Wait until there is at least one GPS payload pending
            self.event.wait()

            while True:  # process all pending GPS payloads
                with self.lock:
                    if not self.pending_gps:
                        self.event.clear()
                        break
                    gps_to_send = list(self.pending_gps)
                    self.pending_gps.clear()

                for gps_data in gps_to_send:
                    if gps_ws.gps_ws_manager.has_clients:
                        # Thread-safe send to GPS clients
                        gps_ws.gps_from_thread(gps_data)

                        if log_ws.log_ws_manager.has_clients:
                            log_ws.log_from_thread(
                                f"[GPS-BROADCAST] Sent GPS data!!!!: {gps_data}",
                                msg_type="log"
                            )
                    else:
                        # No clients: re-add to buffer for next attempt
                        with self.lock:
                            self.pending_gps.append(gps_data)
                        # print("[GPS-BROADCAST] No clients connected, keeping GPS data in buffer")
                        break  # exit for-loop and retry later


# --- Internal broadcaster instance ---
_broadcaster = GPSBroadcaster()

# --- Public function for other modules ---
def add_gps(payload: Dict[str, Any]):
    _broadcaster.add_gps(payload)

# --- Starter for the broadcast loop ---
def start_gps_broadcaster() -> threading.Thread:
    thread = threading.Thread(
        target=_broadcaster._broadcast_loop,
        daemon=True,
        name="GPSBroadcaster"
    )
    thread.start()
    print("[GPS-BROADCAST] Started broadcast thread")
    return thread
