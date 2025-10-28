# ==========================================================
# Archivo: src/Services/request_handlers.py
# Descripción:
#   Handlers de requests WebSocket/HTTP para GPS/RouteManager
#   Funciones puras, sin estado global, con manejo de errores
# ==========================================================

from typing import Dict, Any, List
from datetime import datetime
from src.DB.session import SessionLocal
from src.Repositories.gps_data import (
    get_all_devices,
    get_last_gps_all_devices,
    get_gps_data_in_range_by_device
)

from src.Services.gps_broadcaster import add_gps


# ==========================================================
# Función Auxiliar Global
# ==========================================================
def build_response(action: str, request_id: str, data: Any, status: str = "success") -> Dict[str, Any]:
    """
    Construye respuesta estandarizada.
    """
    return {
        "action": action,
        "request_id": request_id,
        "status": status,
        "data": data
    }


# ==========================================================
# SECCIÓN 2.1: Handlers Simples (sin DB)
# ==========================================================
def handle_ping(params: Dict[str, Any], request_id: str) -> dict:
    """
    Health check simple.
    """
    try:
        return build_response("ping", request_id, "pong")
    except Exception as e:
        return build_response("ping", request_id, {"error": str(e)}, status="error")


# ==========================================================
# SECCIÓN 2.2: Handlers con DB (queries simples)
# ==========================================================
def handle_get_devices(params: Dict[str, Any], request_id: str) -> dict:
    """
    Lista dispositivos registrados en la tabla 'devices'.
    """
    try:
        with SessionLocal() as db:
            devices = get_all_devices(db)
            data = {"devices": devices, "count": len(devices)}
        return build_response("get_devices", request_id, data)
    except Exception as e:
        return build_response("get_devices", request_id, {"error": str(e)}, status="error")


def handle_get_last_positions(params: Dict[str, Any], request_id: str) -> dict:
    """
    Obtiene el último GPS de cada dispositivo.
    """
    try:
        with SessionLocal() as db:
            last_positions = get_last_gps_all_devices(db)
            count = 0
            for device_id, gps_data in last_positions.items():
                add_gps(gps_data)
                count += 1
        return build_response("get_last_positions", request_id, {"message": "Last positions sent", "count": count})
    except Exception as e:
        return build_response("get_last_positions", request_id, {"error": str(e)}, status="error")


# ==========================================================
# SECCIÓN 2.2.5: Handler de Rango de Timestamps (NUEVO)
# ==========================================================
def handle_get_timestamp_range(params: Dict[str, Any], request_id: str) -> dict:
    """
    Obtiene el rango de timestamps disponibles (más antiguo y más nuevo).
    
    Params:
        - device_id: str (opcional)
            - Si se especifica: rango de ese device
            - Si no: rango global de todos los devices activos
    
    Returns:
        {
            "oldest_timestamp": "2025-01-01T00:00:00Z",
            "newest_timestamp": "2025-10-21T15:30:00Z",
            "device_id": "TRUCK-001" o null,
            "span_seconds": 25920000
        }
    """
    try:
        device_id = params.get("device_id")
        
        with SessionLocal() as db:
            if device_id:
                # Rango de un device específico
                from src.Repositories.gps_data import get_oldest_gps_row_by_device, get_last_gps_row_by_device
                oldest = get_oldest_gps_row_by_device(db, device_id)
                newest = get_last_gps_row_by_device(db, device_id)
                
                if not oldest or not newest:
                    return build_response(
                        "get_timestamp_range",
                        request_id,
                        {"error": f"No GPS data for device '{device_id}'"},
                        status="error"
                    )
            else:
                # Rango global
                from src.Repositories.gps_data import get_global_oldest_gps, get_global_newest_gps
                oldest = get_global_oldest_gps(db)
                newest = get_global_newest_gps(db)
                
                if not oldest or not newest:
                    return build_response(
                        "get_timestamp_range",
                        request_id,
                        {"error": "No GPS data available"},
                        status="error"
                    )
            
            # Calcular span
            oldest_dt = datetime.fromisoformat(oldest["Timestamp"].replace("Z", "+00:00"))
            newest_dt = datetime.fromisoformat(newest["Timestamp"].replace("Z", "+00:00"))
            span_seconds = (newest_dt - oldest_dt).total_seconds()
            
            data = {
                "oldest_timestamp": oldest["Timestamp"],
                "newest_timestamp": newest["Timestamp"],
                "device_id": device_id,
                "span_seconds": int(span_seconds)
            }
            
        return build_response("get_timestamp_range", request_id, data)
    
    except Exception as e:
        return build_response(
            "get_timestamp_range",
            request_id,
            {"error": str(e)},
            status="error"
        )


# ==========================================================
# SECCIÓN 2.3: Handler Complejo (history)
# ==========================================================
def handle_get_history(params: Dict[str, Any], request_id: str) -> dict:
    """
    Obtiene histórico GPS entre dos fechas con información de geocerca.
    """
    try:
        start_str = params.get("start")
        end_str = params.get("end")
        device_id = params.get("device_id")
        format_type = params.get("format", "polyline")

        if not start_str or not end_str:
            raise ValueError("Missing 'start' or 'end' parameter")

        start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))

        with SessionLocal() as db:
            if device_id:
                # Histórico de un device específico
                history = get_gps_data_in_range_by_device(db, device_id, start_dt, end_dt)
                
                if format_type == "polyline":
                    polyline = []
                    for p in history:
                        if p.get("Latitude") is None or p.get("Longitude") is None:
                            continue
                        
                        point = {
                            "lat": p["Latitude"],
                            "lon": p["Longitude"],
                            "timestamp": p["Timestamp"]
                        }
                        
                        if p.get("geofence"):
                            point["geofence"] = p["geofence"]
                        
                        polyline.append(point)
                    
                    data = {
                        "device_id": device_id,
                        "start": start_str,
                        "end": end_str,
                        "count": len(polyline),
                        "polyline": polyline
                    }
                else:
                    data = {
                        "device_id": device_id,
                        "start": start_str,
                        "end": end_str,
                        "count": len(history),
                        "history": history
                    }
            else:
                # Histórico de TODOS los devices (legacy)
                from src.Repositories.gps_data import get_gps_data_in_range
                history = get_gps_data_in_range(db, start_dt, end_dt)
                data = {
                    "count": len(history),
                    "history": history
                }
        
        return build_response("get_history", request_id, data)
    
    except Exception as e:
        return build_response(
            "get_history",
            request_id,
            {"error": str(e)},
            status="error"
        )
