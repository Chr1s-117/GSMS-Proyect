# src/Core/request_ws.py
from typing import Dict, Any
from fastapi import WebSocket
from .wsBase import WebSocketManager
from src.Services.response_broadcaster import add_response
from src.Services.gps_broadcaster import add_gps
from src.DB.session import SessionLocal
from src.Repositories.gps_data import (
    get_oldest_gps_row,
    get_last_gps_row,
    get_gps_data_in_range,
)
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
        # Monitores independientes
        self._monitor_lower_task: asyncio.Task | None = None
        self._monitor_upper_task: asyncio.Task | None = None
        self._monitor_lower_active: bool = False
        self._monitor_upper_active: bool = False

        # Últimos valores enviados
        self._last_oldest: dict | None = None
        self._last_newest: dict | None = None

        # request_id asociado a lower_bound
        self._last_lower_request_id: str | None = None

    @property
    def has_clients(self) -> bool:
        return len(self.clients) > 0

    async def _monitor_lower_bound(self):
        """Loop que vigila la fila más antigua (lower bound)."""
        print("[REQUEST-WS] Monitor de lower_bound iniciado")
        while self._monitor_lower_active:
            try:
                with SessionLocal() as db:
                    oldest_row = get_oldest_gps_row(db)

                if oldest_row and oldest_row != self._last_oldest and self._last_lower_request_id:
                    self._last_oldest = oldest_row
                    print(f"[REQUEST-WS] Enviando lower_bound actualizado: {oldest_row}")
                    add_response(build_response("get_lower_bound", self._last_lower_request_id, oldest_row))

            except Exception as e:
                print(f"[REQUEST-WS] Error en _monitor_lower_bound: {e}")

            await asyncio.sleep(0.25)

        print("[REQUEST-WS] Monitor de lower_bound detenido")

    async def _monitor_upper_bound(self):
        """Loop que vigila la fila más reciente (upper bound)."""
        print("[REQUEST-WS] Monitor de upper_bound iniciado")
        while self._monitor_upper_active:
            try:
                with SessionLocal() as db:
                    newest_row = get_last_gps_row(db)

                if newest_row and newest_row != self._last_newest:
                    self._last_newest = newest_row
                    print(f"[REQUEST-WS] Broadcasting upper_bound (GPS): {newest_row}")
                    add_gps(newest_row)

            except Exception as e:
                print(f"[REQUEST-WS] Error en _monitor_upper_bound: {e}")

            await asyncio.sleep(0.25)

        print("[REQUEST-WS] Monitor de upper_bound detenido")

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

        if not action:
            print("[REQUEST-WS] Missing 'action' field")
            return

        # --- Handlers ---
        if action == "ping":
            add_response(build_response(action, request_id, "pong"))

        elif action == "get_lower_bound":
            subscribe = params.get("subscribe", False)
            if subscribe:
                self._last_lower_request_id = request_id
                self._monitor_lower_active = True

                with SessionLocal() as db:
                    oldest_row = get_oldest_gps_row(db)
                if oldest_row:
                    self._last_oldest = oldest_row
                    add_response(build_response("get_lower_bound", request_id, oldest_row))

                if not self._monitor_lower_task or self._monitor_lower_task.done():
                    self._monitor_lower_task = asyncio.create_task(self._monitor_lower_bound())

                print("[REQUEST-WS] Suscripción activada para get_lower_bound")

            else:
                self._monitor_lower_active = False
                self._last_lower_request_id = None
                if self._monitor_lower_task and not self._monitor_lower_task.done():
                    self._monitor_lower_task.cancel()
                    self._monitor_lower_task = None
                print("[REQUEST-WS] Suscripción cancelada para get_lower_bound")

        elif action == "get_upper_bound":
            subscribe = params.get("subscribe", False)
            if subscribe:
                self._monitor_upper_active = True

                with SessionLocal() as db:
                    newest_row = get_last_gps_row(db)
                if newest_row:
                    self._last_newest = newest_row
                    add_gps(newest_row)

                if not self._monitor_upper_task or self._monitor_upper_task.done():
                    self._monitor_upper_task = asyncio.create_task(self._monitor_upper_bound())

                print("[REQUEST-WS] Suscripción activada para get_upper_bound")

            else:
                self._monitor_upper_active = False
                if self._monitor_upper_task and not self._monitor_upper_task.done():
                    self._monitor_upper_task.cancel()
                    self._monitor_upper_task = None
                print("[REQUEST-WS] Suscripción cancelada para get_upper_bound")

        elif action == "get_history":
            try:
                start = params.get("start")
                end = params.get("end")

                if not start or not end:
                    raise ValueError("Missing 'start' or 'end' parameters")

                start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))

                with SessionLocal() as db:
                    history = get_gps_data_in_range(db, start_dt, end_dt)

                add_response(build_response(action, request_id, history))

            except Exception as e:
                print(f"[REQUEST-WS] Error in get_history: {e}")
                add_response(build_response(action, request_id, {"error": str(e)}, status="error"))

        else:
            add_response(build_response(action, request_id, {
                "error": f"Unknown action '{action}'",
                "params": params
            }, status="error"))


# Single instance
request_ws_manager = RequestWebSocketManager()
