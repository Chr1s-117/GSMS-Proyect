# ==========================================================
# Archivo: src/Core/request_ws.py
# Descripción:
#   Gestor WebSocket SIMPLIFICADO (sin monitor)
#   Maneja requests y delega a handlers stateless
# ==========================================================

from typing import Dict, Any
from fastapi import WebSocket
import json
from .wsBase import WebSocketManager
from src.Services.response_broadcaster import add_response
from src.Services import request_handlers as handlers


# ==========================================================
# Clase principal
# ==========================================================
class RequestWebSocketManager(WebSocketManager):
    def __init__(self):
        super().__init__()
        # ✅ LIMPIO: Sin estado, sin monitor, sin cache
        print("[REQUEST-WS] ✅ Inicializado (stateless)")
    
    @property
    def has_clients(self) -> bool:
        return len(self.clients) > 0
    
    # ==========================================================
    # Manejo de mensajes (SIMPLIFICADO)
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
        # TODAS LAS ACCIONES SON SIMPLES (stateless)
        # ======================================================
        SIMPLE_ACTIONS = [
            "ping",
            "get_devices",
            "get_history",
            "get_timestamp_range",
            "get_trips",
            "get_last_positions"  # ✅ AHORA ES SIMPLE
        ]
        
        if action in SIMPLE_ACTIONS:
            handler_map = {
                "ping": handlers.handle_ping,
                "get_devices": handlers.handle_get_devices,
                "get_timestamp_range": handlers.handle_get_timestamp_range,
                "get_history": handlers.handle_get_history,
                "get_trips": handlers.handle_get_trips,
                "get_last_positions": handlers.handle_get_last_positions
            }
            
            response = handler_map[action](params, request_id)
            add_response(response)
            return
        
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
            add_response(handlers.build_response(
                action,
                request_id,
                {"error": f"Unknown action '{action}'"},
                status="error"
            ))


# ==========================================================
# Instancia única global
# ==========================================================
# ==========================================================
# Instancia única global
# ==========================================================
request_ws_manager = RequestWebSocketManager()