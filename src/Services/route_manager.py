# ==========================================================
#  Archivo: src/Services/route_manager.py
#  Descripción:
#     Núcleo del sistema de rutas GPS multi-dispositivo.
#     Gestiona buffers, deduplicación, y rutas ordenadas
#     para cada dispositivo conectado (vehículo, tracker, etc.)
# ==========================================================

from typing import Dict, List, Optional, Set
from datetime import datetime, timezone
import threading


# ==========================================================
# 📐 Clase TracePoint
# ==========================================================
class TracePoint:
    """
    Representa un punto GPS normalizado en el buffer.

    Propósito:
    - Normaliza coordenadas a 6 decimales (~11cm precisión)
    - Permite hashing para deduplicación eficiente
    - Compatible con formato Leaflet ([lat, lon])
    """

    def __init__(self, lat: float, lon: float, timestamp: Optional[datetime] = None):
        self.Latitude = self._normalize(lat)
        self.Longitude = self._normalize(lon)
        self.Timestamp = timestamp

    @staticmethod
    def _normalize(coord: float, decimals: int = 6) -> float:
        factor = 10 ** decimals
        return round(coord * factor) / factor

    def to_list(self) -> list[float]:
        return [self.Latitude, self.Longitude]

    def hash_key(self) -> str:
        ts_str = self.Timestamp.isoformat() if self.Timestamp else ""
        return f"{self.Latitude:.6f}|{self.Longitude:.6f}|{ts_str}"


# ==========================================================
# 🚦 Clase RouteManager
# ==========================================================
class RouteManager:
    """
    Gestiona buffers de rutas GPS multi-dispositivo.

    Características:
    - Thread-safe (usa Lock)
    - Deduplicación O(1) con hash_set
    - Ordenamiento automático por timestamp
    - Limpieza selectiva o total
    """

    def __init__(self):
        self._buffers: Dict[str, List[TracePoint]] = {}
        self._hash_sets: Dict[str, Set[str]] = {}
        self._lock = threading.Lock()
        print("[RouteManager] ✅ Inicializado")

    def add_point(
        self,
        device_id: str,
        lat: float,
        lon: float,
        timestamp: Optional[datetime] = None
    ) -> bool:
        if not (-90 <= lat <= 90):
            print(f"[RouteManager] ⚠️ Latitud inválida ({lat}) para {device_id}")
            return False
        if not (-180 <= lon <= 180):
            print(f"[RouteManager] ⚠️ Longitud inválida ({lon}) para {device_id}")
            return False
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        elif timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        point = TracePoint(lat, lon, timestamp)
        point_hash = point.hash_key()

        with self._lock:
            if device_id not in self._buffers:
                self._buffers[device_id] = []
                self._hash_sets[device_id] = set()
                print(f"[RouteManager] 🆕 Nuevo dispositivo: {device_id}")
            if point_hash in self._hash_sets[device_id]:
                return False

            buffer = self._buffers[device_id]
            insert_pos = self._find_insert_position(buffer, timestamp)
            buffer.insert(insert_pos, point)
            self._hash_sets[device_id].add(point_hash)

            print(f"[RouteManager] 📍 {device_id}: punto añadido en posición {insert_pos}/{len(buffer)}")
            return True

    def _find_insert_position(self, buffer: List[TracePoint], timestamp: datetime) -> int:
        left, right = 0, len(buffer)
        while left < right:
            mid = (left + right) // 2
            mid_ts = buffer[mid].Timestamp
            if mid_ts is None:
                left = mid + 1
            elif mid_ts < timestamp:
                left = mid + 1
            else:
                right = mid
        return left

    def get_route(self, device_id: str) -> dict:
        with self._lock:
            buffer = self._buffers.get(device_id, [])
            polyline = [p.to_list() for p in buffer]
            return {
                "device_id": device_id,
                "count": len(polyline),
                "polyline": polyline
            }

    # ======================================================
    # 🔹 Ajuste 1: Obtener todas las rutas activas
    # ======================================================
    def get_all_routes(self) -> Dict[str, dict]:
        """
        Obtiene rutas de TODOS los dispositivos activos.
        """
        with self._lock:
            return {
                device_id: self.get_route(device_id)
                for device_id in self._buffers.keys()
            }

    def clear_device(self, device_id: str) -> bool:
        with self._lock:
            if device_id in self._buffers:
                del self._buffers[device_id]
                del self._hash_sets[device_id]
                print(f"[RouteManager] 🗑️ Buffer eliminado: {device_id}")
                return True
            return False

    def clear_all_devices(self) -> int:
        with self._lock:
            count = len(self._buffers)
            self._buffers.clear()
            self._hash_sets.clear()
            print(f"[RouteManager] 🧹 Todos los buffers eliminados ({count} devices)")
            return count

    def get_device_count(self) -> int:
        with self._lock:
            return len(self._buffers)

    # ======================================================
    # 🔹 Ajuste 2: Obtener estadísticas globales
    # ======================================================
    def get_stats(self) -> dict:
        with self._lock:
            devices_stats = {
                device_id: len(buffer)
                for device_id, buffer in self._buffers.items()
            }
            return {
                "total_devices": len(self._buffers),
                "total_points": sum(devices_stats.values()),
                "devices": devices_stats
            }


# ==========================================================
# 🌐 Ajuste 3: Instancia global (singleton)
# ==========================================================
route_manager = RouteManager()
