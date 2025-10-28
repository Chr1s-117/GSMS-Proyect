# src/Services/response_broadcaster.py
import threading
from typing import Dict, Any
from src.Core.response_ws import response_from_thread, response_ws_manager


class ResponseBroadcaster:
    """
    Service that manages a buffer of pending responses and
    sends them via ResponseWebSocketManager using the thread-safe entry point.
    """

    def __init__(self):
        self.pending_responses: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        self.event = threading.Event()

    def add_response(self, payload: Dict[str, Any]):
        """Add a response to the buffer and notify the broadcast loop."""
        request_id = payload.get("request_id")
        if not request_id:
            print("[RESPONSE-BROADCAST] Ignored response without request_id")
            return
        with self.lock:
            self.pending_responses[request_id] = payload
            print(f"[RESPONSE-BROADCAST] Added response for request_id {request_id}")
            print(f"[RESPONSE-BROADCAST] Pending responses: {len(self.pending_responses)}")
            self.event.set()  # wake up the broadcast loop

    def _broadcast_loop(self):
        """Continuously tries to send pending responses if clients are connected."""
        while True:
            # Wait until there is at least one response pending
            self.event.wait()

            while True:  # process all pending responses
                with self.lock:
                    if not self.pending_responses:
                        self.event.clear()
                        break
                    responses_to_send = list(self.pending_responses.values())
                    self.pending_responses.clear()

                for resp in responses_to_send:
                    if response_ws_manager.has_clients:
                        # Always use thread-safe send method
                        response_from_thread(resp)
                    else:
                        # No clients: re-add to buffer for next attempt
                        with self.lock:
                            self.pending_responses[resp["request_id"]] = resp
                        print(f"[RESPONSE-BROADCAST] No clients connected, keeping response in buffer")
                        break  # exit for-loop and retry later

# --- Internal broadcaster instance ---
_broadcaster = ResponseBroadcaster()

# --- Public function for other modules ---
def add_response(payload: Dict[str, Any]):
    _broadcaster.add_response(payload)

# --- Starter for the broadcast loop ---
def start_response_broadcaster() -> threading.Thread:
    thread = threading.Thread(
        target=_broadcaster._broadcast_loop,
        daemon=True,
        name="ResponseBroadcaster"
    )
    thread.start()
    print("[RESPONSE-BROADCAST] Started broadcast thread")
    return thread
