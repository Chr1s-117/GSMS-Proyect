# src/Services/ddns.py

import requests
import socket
import time
import threading
from src.Core import log_ws  # logger centralizado

# Configuración Dynu (rellena con tus valores)
DYNU_HOST = "Iphost1.mywire.org"
DYNU_USER = "Ip1update"
DYNU_PASS = "PK#qqdROqMeP"
CHECK_INTERVAL = 10  # 10 segundos

def update_dynu_ip():
    """
    Loop infinito que revisa la IP pública y actualiza Dynu si cambió.
    Todos los mensajes se envían como logs JSON válidos.

    """
    while True:
        try:
            current_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
            log_ws.log_from_thread(f"[Dynu] Current public IP: {current_ip}", msg_type="log")
            

            try:
                dynu_ip = socket.gethostbyname(DYNU_HOST)
                log_ws.log_from_thread(f"[DNS] Current IP for {DYNU_HOST}: {dynu_ip}", msg_type="log")

                if dynu_ip != current_ip:
                    url = f"https://api.dynu.com/nic/update?hostname={DYNU_HOST}&myip={current_ip}"
                    try:
                        response = requests.get(url, auth=(DYNU_USER, DYNU_PASS))
                        print(f"[Dynu] Response: {response.text.strip()}")
                        log_ws.log_from_thread(f"[Dynu] Response: {response.text.strip()}", msg_type="log")
                        
                    except Exception as e:
                        log_ws.log_from_thread(f"[Dynu] Error updating IP for {DYNU_HOST}: {e}", msg_type="log")
                else:
                    print(f"[Dynu] IP for {DYNU_HOST} is up-to-date.")
                    log_ws.log_from_thread(f"[Dynu] IP for {DYNU_HOST} is up-to-date.", msg_type="log")

            except Exception as e:
                log_ws.log_from_thread(f"[Dynu] Error fetching IP for {DYNU_HOST}: {e}", msg_type="log")

        except Exception as e:
            log_ws.log_from_thread(f"[Dynu] Error fetching current public IP: {e}", msg_type="log")

        time.sleep(CHECK_INTERVAL)


def start_ddns_service() -> threading.Thread:
    """
    Lanza update_dynu_ip en un hilo daemon.
    Devuelve el objeto Thread.
    """
    thread = threading.Thread(target=update_dynu_ip, daemon=True, name="DDNS-Service")
    thread.start()

    print("[DDNS] Background DDNS thread started")
    
    return thread
