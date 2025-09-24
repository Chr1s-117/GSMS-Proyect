# src/Core/request_ws.py
from typing import Dict, Any
from fastapi import WebSocket
from .wsBase import WebSocketManager
from src.Services.response_broadcaster import add_response
from src.DB.session import SessionLocal
from src.Repositories.gps_data import get_oldest_gps_row, get_gps_data_in_range
from datetime import datetime
import json
import asyncio

def build_response(action: str, request_id: str, data: Any, status: str = "success") -> Dict[str, Any]:
    return {
        "action": action,
        "request_id": request_id,
        "status": status,
        "data": data
    }

class RequestWebSocketManager(WebSocketManager):
    def __init__(self):
        super().__init__()
        self._monitor_task: asyncio.Task | None = None
        self._monitor_active: bool = False
        self._last_oldest: dict | None = None
        self._last_request_id: str | None = None

    @property
    def has_clients(self) -> bool:
        return len(self.clients) > 0

    async def _monitor_history_bounds(self):
        """
        Loop que vigila la fila más antigua.
        Mientras _monitor_active=True, revisa cambios y notifica.
        """
        print("[REQUEST-WS] Monitor de history_bounds iniciado")
        while self._monitor_active:
            try:
                with SessionLocal() as db:
                    oldest_row = get_oldest_gps_row(db)

                # Solo notificamos si cambió y tenemos request_id válido
                if oldest_row and oldest_row != self._last_oldest and self._last_request_id:
                    self._last_oldest = oldest_row
                    print(f"[REQUEST-WS] Enviando bounds actualizados: {oldest_row}")
                    add_response(build_response("get_history_bounds", self._last_request_id, oldest_row))

            except Exception as e:
                print(f"[REQUEST-WS] Error en _monitor_history_bounds: {e}")

            # Evitar loop apretado, revisamos cada 250ms
            await asyncio.sleep(0.25)

        print("[REQUEST-WS] Monitor de history_bounds detenido")

    async def handle_message(self, ws: WebSocket, message: str):
        print(f"[REQUEST-WS] Received raw message: {message}")

        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            print(f"[REQUEST-WS] Invalid JSON: {message}")
            return

        print(f"[REQUEST-WS] Parsed JSON: {data}")

        action = data.get("action")
        request_id = data.get("request_id")
        params: Dict[str, Any] = data.get("params", {})

        print(f"[REQUEST-WS] Action: {action}, Request ID: {request_id}, Params: {params}")

        if not action:
            print("[REQUEST-WS] Missing 'action' field")
            return

        # --- Handlers ---
        if action == "ping":
            add_response(build_response(action, request_id, "pong"))

        elif action == "get_history_bounds":
            subscribe = params.get("subscribe", False)

            if subscribe:
                # Guardamos el request_id para las notificaciones futuras
                self._last_request_id = request_id
                self._monitor_active = True

                # Enviar el valor inicial de oldest_row inmediatamente
                with SessionLocal() as db:
                    oldest_row = get_oldest_gps_row(db)
                if oldest_row:
                    self._last_oldest = oldest_row
                    print(f"[REQUEST-WS] Enviando bounds iniciales: {oldest_row}")
                    add_response(build_response("get_history_bounds", request_id, oldest_row))

                # Iniciar monitor si no está ya corriendo
                if not self._monitor_task or self._monitor_task.done():
                    self._monitor_task = asyncio.create_task(self._monitor_history_bounds())

                print("[REQUEST-WS] Suscripción activada para get_history_bounds")

            else:
                # Desuscribir: detener monitor y limpiar tarea
                self._monitor_active = False
                self._last_request_id = None
                if self._monitor_task and not self._monitor_task.done():
                    self._monitor_task.cancel()
                    self._monitor_task = None
                print("[REQUEST-WS] Suscripción cancelada para get_history_bounds")

        elif action == "get_history":
            try:
                print(f"[REQUEST-WS] Params for get_history: {params}")

                start = params.get("start")
                end = params.get("end")

                print(f"[REQUEST-WS] Extracted 'start': {start}, 'end': {end}")

                if not start or not end:
                    raise ValueError("Missing 'start' or 'end' parameters")

                # convertir ISO8601 a datetime
                start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))

                print(f"[REQUEST-WS] Converted datetimes -> start: {start_dt}, end: {end_dt}")

                with SessionLocal() as db:
                    history = get_gps_data_in_range(db, start_dt, end_dt)

                print(f"[REQUEST-WS] Retrieved {len(history)} rows from DB")
                add_response(build_response(action, request_id, history))

            except Exception as e:
                print(f"[REQUEST-WS] Error in get_history: {e}")
                add_response(build_response(action, request_id, {"error": str(e)}, status="error"))

        else:
            print(f"[REQUEST-WS] Unknown action '{action}' with params {params}")
            add_response(build_response(action, request_id, {
                "error": f"Unknown action '{action}'",
                "params": params
            }, status="error"))

# Single instance
request_ws_manager = RequestWebSocketManager()
