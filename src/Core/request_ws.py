# ==========================================================
# Archivo: src/Core/request_ws.py
# Descripción:
#   Gestor WebSocket que delega toda la lógica de negocio
#   a src/Services/request_handlers.py
#   Mantiene control de monitores (last_positions)
# ==========================================================

from typing import Dict, Any
from fastapi import WebSocket
import asyncio
import json
from datetime import datetime
from .wsBase import WebSocketManager
from src.Services.response_broadcaster import add_response
from src.Services.gps_broadcaster import add_gps
from src.DB.session import SessionLocal
from src.Repositories.gps_data import (
    get_last_gps_all_devices
)
from src.Services import request_handlers as handlers


# ==========================================================
# Clase principal
# ==========================================================
class RequestWebSocketManager(WebSocketManager):
    def __init__(self):
        super().__init__()
        # Monitores
        self._monitor_last_positions_task: asyncio.Task | None = None
        self._monitor_last_positions_active: bool = False

        # Cache de estados
        self._last_positions: dict = {}

    @property
    def has_clients(self) -> bool:
        return len(self.clients) > 0

    # ==========================================================
    # 🔹 ÚNICO monitor activo: _monitor_last_positions
    # ==========================================================
    async def _monitor_last_positions(self):
        """
        Monitorea última posición de TODOS los devices activos.
        Este es el ÚNICO monitor necesario para GPS en tiempo real.
        """
        print("[REQUEST-WS] Monitor de last_positions iniciado")
        while self._monitor_last_positions_active:
            try:
                with SessionLocal() as db:
                    current_positions = get_last_gps_all_devices(db)
                
                for device_id, gps_data in current_positions.items():
                    if device_id not in self._last_positions or \
                       self._last_positions[device_id] != gps_data:
                        add_gps(gps_data)
                        self._last_positions[device_id] = gps_data
                
                # Detectar devices eliminados
                removed = set(self._last_positions.keys()) - set(current_positions.keys())
                for device_id in removed:
                    del self._last_positions[device_id]
            
            except Exception as e:
                print(f"[REQUEST-WS] Error en _monitor_last_positions: {e}")
            
            await asyncio.sleep(0.5)
        
        print("[REQUEST-WS] Monitor de last_positions detenido")

    # ==========================================================
    # Manejo de mensajes (FASE 7)
    # ==========================================================
    async def handle_message(self, ws: WebSocket, message: str):
        print(f"[REQUEST-WS] Received raw message: {message}")

        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            print(f"[REQUEST-WS] Invalid JSON: {message}")
            return

        action = data.get("action")
        request_id = data.get("request_id")
        params: Dict[str, Any] = data.get("params", {})

        if not action:
            print("[REQUEST-WS] Missing 'action' field")
            return

        # ======================================================
        # ACCIONES SIMPLES (FASE 7)
        # ======================================================
        SIMPLE_ACTIONS = [
            "ping",
            "get_devices",
            "get_history",
            "get_timestamp_range"
        ]

        if action in SIMPLE_ACTIONS:
            handler_map = {
                "ping": handlers.handle_ping,
                "get_devices": handlers.handle_get_devices,
                "get_history": handlers.handle_get_history,
                "get_timestamp_range": handlers.handle_get_timestamp_range
            }
            response = handler_map[action](params, request_id)
            add_response(response)
            return

        # ======================================================
        # get_last_positions (con suscripción)
        # ======================================================
        elif action == "get_last_positions":
            response = handlers.handle_get_last_positions(params, request_id)
            add_response(response)

            subscribe = params.get("subscribe", False)
            if subscribe:
                self._monitor_last_positions_active = True
                if not self._monitor_last_positions_task or self._monitor_last_positions_task.done():
                    self._monitor_last_positions_task = asyncio.create_task(self._monitor_last_positions())
                print("[REQUEST-WS] ✅ Monitor last_positions activado")
            else:
                self._monitor_last_positions_active = False
                if self._monitor_last_positions_task and not self._monitor_last_positions_task.done():
                    self._monitor_last_positions_task.cancel()
                    self._monitor_last_positions_task = None
                print("[REQUEST-WS] ❌ Monitor last_positions desactivado")

        # ======================================================
        # Acción desconocida
        # ======================================================
        else:
            add_response(handlers.build_response(
                action,
                request_id,
                {"error": f"Unknown action '{action}'"},
                status="error"
            ))


# ==========================================================
# Instancia única global
# ==========================================================
request_ws_manager = RequestWebSocketManager()
