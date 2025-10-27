# src/Services/ddns.py

"""
DDNS Service for Automatic Dynu IP Updates

This module implements a dynamic DNS updater using the Dynu service.
It periodically checks the public IP of the server and updates the
Dynu hostname if the IP has changed. All actions and errors are
logged centrally using the log_ws module.

Key features:
- Periodic public IP check (configurable interval).
- Updates Dynu hostname only if the IP has changed.
- Centralized logging for monitoring and debugging.
- Runs in a daemon thread for asynchronous operation.
"""

import requests
import socket
import time
import threading
from src.Core import log_ws  # Centralized logger

# --------------------------
# Dynu Configuration
# --------------------------
DYNU_HOST = "Iphost1.mywire.org"  # Hostname managed in Dynu
DYNU_USER = "Ip1update"           # Dynu username
DYNU_PASS = "PK#qqdROqMeP"        # Dynu password/API key
CHECK_INTERVAL = 10                # Interval between checks (seconds)

# --------------------------
# Main DDNS Update Loop
# --------------------------
def update_dynu_ip():
    """
    Infinite loop that monitors the server's public IP and updates
    the Dynu hostname if it changes.

    Steps:
    1. Fetch current public IP from https://api.ipify.org.
    2. Resolve the Dynu hostname to check current DNS IP.
    3. Compare the IPs; if different, send an authenticated Dynu update request.
    4. Log all activity and errors via log_ws.
    5. Sleep for the configured interval before repeating.
    """
    while True:
        try:
            # Get current public IP
            current_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
            log_ws.log_from_thread(f"[Dynu] Current public IP: {current_ip}", msg_type="log")

            try:
                # Resolve Dynu hostname
                dynu_ip = socket.gethostbyname(DYNU_HOST)
                log_ws.log_from_thread(f"[DNS] Current IP for {DYNU_HOST}: {dynu_ip}", msg_type="log")

                # Update Dynu if IP has changed
                if dynu_ip != current_ip:
                    url = f"https://api.dynu.com/nic/update?hostname={DYNU_HOST}&myip={current_ip}"
                    try:
                        response = requests.get(url, auth=(DYNU_USER, DYNU_PASS))
                        print(f"[Dynu] Response: {response.text.strip()}")
                        log_ws.log_from_thread(f"[Dynu] Response: {response.text.strip()}", msg_type="log")
                    except Exception as e:
                        log_ws.log_from_thread(f"[Dynu] Error updating IP for {DYNU_HOST}: {e}", msg_type="log")
                else:
                    # IP unchanged; no update needed
                    print(f"[Dynu] IP for {DYNU_HOST} is up-to-date.")
                    log_ws.log_from_thread(f"[Dynu] IP for {DYNU_HOST} is up-to-date.", msg_type="log")

            except Exception as e:
                log_ws.log_from_thread(f"[Dynu] Error fetching IP for {DYNU_HOST}: {e}", msg_type="log")

        except Exception as e:
            log_ws.log_from_thread(f"[Dynu] Error fetching current public IP: {e}", msg_type="log")

        # Wait before next check
        time.sleep(CHECK_INTERVAL)

# --------------------------
# Public API to Start Service
# --------------------------
def start_ddns_service() -> threading.Thread:
    """
    Launches the DDNS service in a daemon thread.

    Returns:
        threading.Thread: The background DDNS service thread.
    """
    thread = threading.Thread(target=update_dynu_ip, daemon=True, name="DDNS-Service")
    thread.start()

    print("[DDNS] Background DDNS thread started")
    
    return thread