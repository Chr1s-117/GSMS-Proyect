# ==========================================================
#  Archivo: src/Services/route_manager.py
#  Descripción:
#     Multi-device GPS route management system core.
#     Manages in-memory buffers, deduplication, and ordered routes
#     for each connected device (vehicle, tracker, etc.)
#
#  Architecture:
#     - Thread-safe operations with Lock
#     - O(1) deduplication using hash sets
#     - Automatic timestamp-based ordering
#     - Per-device route isolation
#     - Memory-efficient point storage
#
#  Use Cases:
#     - Real-time route visualization on map
#     - GPS trail rendering for multiple devices
#     - Route playback and analysis
#     - Deduplication of redundant GPS points
# ==========================================================

from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime, timezone
import threading


# ==========================================================
# 📐 TracePoint Class
# ==========================================================

class TracePoint:
    """
    Normalized GPS point representation for route buffers.

    Purpose:
    - Normalize coordinates to 6 decimal places (~11cm precision)
    - Enable efficient deduplication via hashing
    - Compatible with Leaflet/mapping libraries ([lat, lon] format)
    - Memory-efficient storage (only lat, lon, timestamp)

    Precision:
    - 6 decimals: ~0.11 meters (sufficient for vehicle tracking)
    - 5 decimals: ~1.1 meters
    - 4 decimals: ~11 meters

    Example:
        point = TracePoint(10.987654321, -74.789012345, datetime.now(timezone.utc))
        # Stored as: Latitude=10.987654, Longitude=-74.789012
        
        leaflet_format = point.to_list()
        # [10.987654, -74.789012]
        
        hash_key = point.hash_key()
        # "10.987654|-74.789012|2025-10-22T09:54:46+00:00"
    """

    def __init__(
        self, 
        lat: float, 
        lon: float, 
        timestamp: Optional[datetime] = None,
        geofence: Optional[dict] = None
    ):
        """
        Initialize a GPS trace point.

        Args:
            lat: Latitude in decimal degrees (-90 to 90)
            lon: Longitude in decimal degrees (-180 to 180)
            timestamp: UTC timestamp of GPS reading (default: now)
            geofence: Optional geofence information dict
                {
                    "id": "warehouse-001",
                    "name": "Main Warehouse",
                    "event": "entry" | "exit" | "inside"
                }
        """
        self.Latitude = self._normalize(lat)
        self.Longitude = self._normalize(lon)
        self.Timestamp = timestamp
        self.geofence = geofence  # NEW: Store geofence info

    @staticmethod
    def _normalize(coord: float, decimals: int = 6) -> float:
        """
        Normalize coordinate to specified decimal places.

        Uses round() for consistent precision and memory efficiency.
        
        Args:
            coord: Raw coordinate value
            decimals: Number of decimal places (default: 6)
            
        Returns:
            Normalized coordinate
            
        Example:
            _normalize(10.987654321) -> 10.987654
        """
        factor = 10 ** decimals
        return round(coord * factor) / factor

    def to_list(self) -> List[float]:
        """
        Convert to [lat, lon] format for Leaflet/mapping libraries.

        Returns:
            [latitude, longitude]
            
        Example:
            point.to_list() -> [10.987654, -74.789012]
        """
        return [self.Latitude, self.Longitude]

    def to_dict(self) -> dict:
        """
        Convert to dictionary with all fields.

        Returns:
            Dictionary with lat, lon, timestamp, and optional geofence
            
        Example:
            {
                "lat": 10.987654,
                "lon": -74.789012,
                "timestamp": "2025-10-22T09:54:46Z",
                "geofence": {
                    "id": "warehouse-001",
                    "name": "Main Warehouse",
                    "event": "entry"
                }
            }
        """
        result = {
            "lat": self.Latitude,
            "lon": self.Longitude,
            "timestamp": self.Timestamp.isoformat() if self.Timestamp else None
        }
        
        if self.geofence:
            result["geofence"] = self.geofence
        
        return result

    def hash_key(self) -> str:
        """
        Generate unique hash key for deduplication.

        Combines latitude, longitude, and timestamp to create unique identifier.
        Used in hash set for O(1) duplicate detection.

        Returns:
            Hash string in format "lat|lon|timestamp"
            
        Example:
            "10.987654|-74.789012|2025-10-22T09:54:46+00:00"
        """
        ts_str = self.Timestamp.isoformat() if self.Timestamp else ""
        return f"{self.Latitude:.6f}|{self.Longitude:.6f}|{ts_str}"

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<TracePoint(lat={self.Latitude}, lon={self.Longitude}, ts={self.Timestamp})>"


# ==========================================================
# 🚦 RouteManager Class
# ==========================================================

class RouteManager:
    """
    Thread-safe multi-device GPS route buffer manager.

    This class maintains in-memory buffers of GPS points for multiple devices,
    providing real-time route visualization and analysis capabilities.

    Features:
    - Thread-safe operations (all methods protected by Lock)
    - O(1) deduplication using hash sets
    - Automatic chronological ordering via binary search insertion
    - Per-device route isolation (separate buffers)
    - Memory-efficient point storage
    - Selective or bulk buffer clearing
    - Statistics and monitoring

    Architecture:
    - _buffers: Dict[device_id, List[TracePoint]] - Ordered point lists
    - _hash_sets: Dict[device_id, Set[hash_key]] - O(1) duplicate detection
    - _lock: threading.Lock - Thread synchronization

    Thread Safety:
    All public methods acquire _lock before accessing shared state,
    ensuring safe concurrent access from multiple threads (WebSocket, UDP, etc.)

    Memory Usage:
    - ~40 bytes per TracePoint (lat, lon, timestamp, geofence ref)
    - 1000 points per device ≈ 40 KB
    - 100 devices × 1000 points ≈ 4 MB

    Example:
        manager = RouteManager()
        
        # Add points
        manager.add_point("TRUCK-001", 10.9878, -74.7889, datetime.now(timezone.utc))
        manager.add_point("TRUCK-002", 10.9880, -74.7890, datetime.now(timezone.utc))
        
        # Get route
        route = manager.get_route("TRUCK-001")
        # {"device_id": "TRUCK-001", "count": 500, "polyline": [[lat, lon], ...]}
        
        # Get stats
        stats = manager.get_stats()
        # {"total_devices": 2, "total_points": 1500, "devices": {...}}
    """

    def __init__(self):
        """
        Initialize RouteManager with empty buffers and hash sets.
        """
        # Per-device ordered point buffers
        self._buffers: Dict[str, List[TracePoint]] = {}
        
        # Per-device hash sets for O(1) duplicate detection
        self._hash_sets: Dict[str, Set[str]] = {}
        
        # Thread synchronization lock
        self._lock = threading.Lock()
        
        print("[RouteManager] ✅ Initialized (multi-device GPS route manager)")

    def add_point(
        self,
        device_id: str,
        lat: float,
        lon: float,
        timestamp: Optional[datetime] = None,
        geofence: Optional[dict] = None
    ) -> bool:
        """
        Add GPS point to device's route buffer with automatic ordering and deduplication.

        This method:
        1. Validates coordinate ranges
        2. Creates/normalizes TracePoint
        3. Checks for duplicates (O(1) via hash set)
        4. Finds insertion position (O(log n) binary search)
        5. Inserts point maintaining chronological order
        6. Updates hash set

        Args:
            device_id: Unique device identifier (e.g., "TRUCK-001")
            lat: Latitude in decimal degrees (-90 to 90)
            lon: Longitude in decimal degrees (-180 to 180)
            timestamp: UTC timestamp (default: now)
            geofence: Optional geofence info dict
                {
                    "id": "warehouse-001",
                    "name": "Main Warehouse",
                    "event": "entry" | "exit" | "inside"
                }

        Returns:
            True if point was added, False if duplicate or invalid

        Example:
            # Add point without geofence
            success = manager.add_point("TRUCK-001", 10.9878, -74.7889)
            
            # Add point with geofence
            success = manager.add_point(
                "TRUCK-001", 
                10.9878, 
                -74.7889,
                datetime.now(timezone.utc),
                geofence={"id": "warehouse-001", "name": "Main Warehouse", "event": "entry"}
            )
        """
        # Validate latitude range
        if not (-90 <= lat <= 90):
            print(f"[RouteManager] ⚠️ Invalid latitude ({lat}) for device {device_id}")
            return False

        # Validate longitude range
        if not (-180 <= lon <= 180):
            print(f"[RouteManager] ⚠️ Invalid longitude ({lon}) for device {device_id}")
            return False

        # Set default timestamp if not provided
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        elif timestamp.tzinfo is None:
            # Assume UTC if naive datetime
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        # Create normalized point
        point = TracePoint(lat, lon, timestamp, geofence)
        point_hash = point.hash_key()

        with self._lock:
            # Initialize buffers for new device
            if device_id not in self._buffers:
                self._buffers[device_id] = []
                self._hash_sets[device_id] = set()
                print(f"[RouteManager] 🆕 New device registered: {device_id}")

            # Check for duplicate (O(1))
            if point_hash in self._hash_sets[device_id]:
                # Duplicate detected - skip
                return False

            # Find insertion position to maintain chronological order (O(log n))
            buffer = self._buffers[device_id]
            insert_pos = self._find_insert_position(buffer, timestamp)

            # Insert point at correct position
            buffer.insert(insert_pos, point)

            # Add to hash set for future duplicate detection
            self._hash_sets[device_id].add(point_hash)

            print(
                f"[RouteManager] 📍 {device_id}: Point added at position "
                f"{insert_pos}/{len(buffer)} (total: {len(buffer)} points)"
            )
            return True

    def _find_insert_position(
        self, 
        buffer: List[TracePoint], 
        timestamp: datetime
    ) -> int:
        """
        Find correct insertion position to maintain chronological order.

        Uses binary search for O(log n) performance.
        Points without timestamps are placed at the end.

        Args:
            buffer: Ordered list of TracePoints
            timestamp: Timestamp of point to insert

        Returns:
            Index where point should be inserted

        Example:
            buffer = [point1(ts=10:00), point2(ts=10:02), point3(ts=10:05)]
            _find_insert_position(buffer, datetime(10:03))
            # Returns: 2 (insert between point2 and point3)
        """
        left, right = 0, len(buffer)

        while left < right:
            mid = (left + right) // 2
            mid_ts = buffer[mid].Timestamp

            if mid_ts is None:
                # Point without timestamp - move right
                left = mid + 1
            elif mid_ts < timestamp:
                left = mid + 1
            else:
                right = mid

        return left

    def get_route(self, device_id: str, include_geofences: bool = True) -> dict:
        """
        Get complete route for a specific device.

        Args:
            device_id: Device identifier
            include_geofences: Include geofence info in points (default: True)

        Returns:
            Dictionary with device route:
            {
                "device_id": "TRUCK-001",
                "count": 500,
                "polyline": [[lat, lon], ...],  // If include_geofences=False
                "points": [{lat, lon, timestamp, geofence}, ...]  // If include_geofences=True
            }

        Example:
            # Simple polyline (no geofences)
            route = manager.get_route("TRUCK-001", include_geofences=False)
            # {"device_id": "TRUCK-001", "count": 500, "polyline": [[10.9878, -74.7889], ...]}

            # Full data with geofences
            route = manager.get_route("TRUCK-001", include_geofences=True)
            # {"device_id": "TRUCK-001", "count": 500, "points": [{lat, lon, timestamp, geofence}, ...]}
        """
        with self._lock:
            buffer = self._buffers.get(device_id, [])

            if include_geofences:
                # Return full point data with geofences
                points = [p.to_dict() for p in buffer]
                return {
                    "device_id": device_id,
                    "count": len(points),
                    "points": points
                }
            else:
                # Return simple polyline (lat/lon only)
                polyline = [p.to_list() for p in buffer]
                return {
                    "device_id": device_id,
                    "count": len(polyline),
                    "polyline": polyline
                }

    def get_all_routes(self, include_geofences: bool = True) -> Dict[str, dict]:
        """
        Get routes for ALL active devices.

        Args:
            include_geofences: Include geofence info in points (default: True)

        Returns:
            Dictionary mapping device_id to route data:
            {
                "TRUCK-001": {"device_id": "TRUCK-001", "count": 500, "points": [...]},
                "TRUCK-002": {"device_id": "TRUCK-002", "count": 300, "points": [...]}
            }

        Example:
            all_routes = manager.get_all_routes(include_geofences=True)
            for device_id, route in all_routes.items():
                print(f"Device {device_id}: {route['count']} points")
        """
        with self._lock:
            return {
                device_id: self.get_route(device_id, include_geofences)
                for device_id in self._buffers.keys()
            }

    def clear_device(self, device_id: str) -> bool:
        """
        Clear route buffer for specific device.

        Args:
            device_id: Device identifier to clear

        Returns:
            True if device buffer was cleared, False if device not found

        Example:
            success = manager.clear_device("TRUCK-001")
            if success:
                print("Buffer cleared")
        """
        with self._lock:
            if device_id in self._buffers:
                point_count = len(self._buffers[device_id])
                del self._buffers[device_id]
                del self._hash_sets[device_id]
                print(f"[RouteManager] 🗑️ Buffer cleared for device {device_id} ({point_count} points removed)")
                return True
            print(f"[RouteManager] ⚠️ Device {device_id} not found (nothing to clear)")
            return False

    def clear_all_devices(self) -> int:
        """
        Clear all device buffers (global reset).

        Returns:
            Number of devices cleared

        Example:
            count = manager.clear_all_devices()
            print(f"Cleared {count} device buffers")
        """
        with self._lock:
            device_count = len(self._buffers)
            total_points = sum(len(buffer) for buffer in self._buffers.values())

            self._buffers.clear()
            self._hash_sets.clear()

            print(
                f"[RouteManager] 🧹 All buffers cleared "
                f"({device_count} devices, {total_points} total points)"
            )
            return device_count

    def get_device_count(self) -> int:
        """
        Get number of active devices with routes in memory.

        Returns:
            Number of devices

        Example:
            count = manager.get_device_count()
            print(f"Tracking {count} devices")
        """
        with self._lock:
            return len(self._buffers)

    def get_stats(self) -> dict:
        """
        Get comprehensive statistics about all routes.

        Returns:
            Dictionary with statistics:
            {
                "total_devices": 10,
                "total_points": 5000,
                "average_points_per_device": 500.0,
                "devices": {
                    "TRUCK-001": 500,
                    "TRUCK-002": 300,
                    ...
                }
            }

        Example:
            stats = manager.get_stats()
            print(f"Total devices: {stats['total_devices']}")
            print(f"Total points: {stats['total_points']}")
            print(f"Average: {stats['average_points_per_device']:.1f} points/device")
        """
        with self._lock:
            devices_stats = {
                device_id: len(buffer)
                for device_id, buffer in self._buffers.items()
            }

            total_points = sum(devices_stats.values())
            total_devices = len(devices_stats)

            return {
                "total_devices": total_devices,
                "total_points": total_points,
                "average_points_per_device": (
                    total_points / total_devices if total_devices > 0 else 0.0
                ),
                "devices": devices_stats
            }

    def has_device(self, device_id: str) -> bool:
        """
        Check if device has active route buffer.

        Args:
            device_id: Device identifier

        Returns:
            True if device exists in buffers, False otherwise

        Example:
            if manager.has_device("TRUCK-001"):
                route = manager.get_route("TRUCK-001")
        """
        with self._lock:
            return device_id in self._buffers

    def get_point_count(self, device_id: str) -> int:
        """
        Get number of points in device's route buffer.

        Args:
            device_id: Device identifier

        Returns:
            Number of points (0 if device not found)

        Example:
            count = manager.get_point_count("TRUCK-001")
            print(f"Device has {count} GPS points")
        """
        with self._lock:
            buffer = self._buffers.get(device_id, [])
            return len(buffer)


# ==========================================================
# 🌐 Global Singleton Instance
# ==========================================================
"""
Global RouteManager instance for application-wide route management.

This singleton is shared across all threads and provides centralized
route buffer management for all GPS-enabled devices.

Usage:
    from src.Services.route_manager import route_manager
    
    # Add point
    route_manager.add_point("TRUCK-001", 10.9878, -74.7889, datetime.now(timezone.utc))
    
    # Get route
    route = route_manager.get_route("TRUCK-001")
    
    # Get stats
    stats = route_manager.get_stats()
"""
route_manager = RouteManager()