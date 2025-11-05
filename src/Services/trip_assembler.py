"""
Trip Assembler Service - Constructs complete trip JSON responses.

Responsibilities:
    - Merge GPS + Accelerometer data for complete routes
    - Build trip metadata with metrics
    - Generate summary statistics
    - Handle null cases (no accel, no geofence, active trips)

Usage:
    from src.Services.trip_assembler import trip_assembler
    
    data = trip_assembler.build_trips_response(db, trips)
"""

from typing import Any, Optional
from sqlalchemy.orm import Session
from src.Models.trip import Trip
from src.Repositories.gps_data import get_full_gps_data_for_trip
from src.Repositories.accelerometer_data import get_accel_map_for_trip


class TripAssembler:
    """
    Assembles complete trip JSON with GPS + accelerometer + geofences.
    
    Core functionality:
        - build_full_trip_json(): Single trip → Complete JSON
        - build_trips_response(): Multiple trips → Response with summary
    """
    
    def build_full_trip_json(
        self,
        db: Session,
        trip: Trip
    ) -> dict[str, Any]:
        """
        Build complete JSON for a single trip.
        
        Args:
            db: SQLAlchemy session
            trip: Trip ORM object
        
        Returns:
            dict: Complete trip data:
            {
                "trip_id": "TRIP_20250101_ESP001_001",
                "device_id": "ESP001",
                "type": "movement",
                "status": "closed",
                "start_time": "2025-01-01T08:00:00Z",
                "end_time": "2025-01-01T08:30:00Z",
                "metrics": {
                    "distance_m": 5420.5,
                    "duration_s": 1800.0,
                    "avg_speed_kmh": 10.84,
                    "point_count": 360
                },
                "route": [...]  # GPS + accel + geofence
            }
        
        Notes:
            - Active trips have end_time: null (not omitted)
            - GPS without accel have accel: null
            - GPS without geofence have geofence: null
        """
        # ========================================
        # Extract trip metadata (safe ORM access)
        # ========================================
        trip_id = str(getattr(trip, 'trip_id', ''))
        device_id = str(getattr(trip, 'device_id', ''))
        trip_type = str(getattr(trip, 'trip_type', 'movement'))
        status = str(getattr(trip, 'status', 'active'))
        
        # Timestamps
        start_time = getattr(trip, 'start_time', None)
        end_time = getattr(trip, 'end_time', None)
        
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ") if start_time else None
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ") if end_time else None
        
        # ========================================
        # Build metrics object
        # ========================================
        metrics = {
            "distance_m": float(getattr(trip, 'distance', 0.0) or 0.0),
            "duration_s": float(getattr(trip, 'duration', 0.0) or 0.0),
            "avg_speed_kmh": float(getattr(trip, 'avg_speed', 0.0) or 0.0),
            "point_count": int(getattr(trip, 'point_count', 0))
        }
        
        # ========================================
        # Load GPS data for this trip
        # ========================================
        gps_data = get_full_gps_data_for_trip(db, trip_id)
        
        # ========================================
        # Load Accel data for this trip
        # ========================================
        accel_map = get_accel_map_for_trip(db, trip_id)
        
        # ========================================
        # Merge GPS + Accel into route
        # ========================================
        route = []
        
        for gps_point in gps_data:
            timestamp = gps_point['timestamp']
            
            # Check if this GPS has accel data
            accel_data = accel_map.get(timestamp, None)
            
            # Build complete route point
            point = {
                "timestamp": timestamp,
                "gps": gps_point['gps'],  # Already has only lat/lon
                "geofence": gps_point['geofence'],  # Can be None
                "accel": accel_data  # Can be None
            }
            
            route.append(point)
        
        # ========================================
        # Assemble final trip JSON
        # ========================================
        return {
            "trip_id": trip_id,
            "device_id": device_id,
            "type": trip_type,
            "status": status,
            "start_time": start_time_str,
            "end_time": end_time_str,  # null for active trips
            "metrics": metrics,
            "route": route
        }
    
    def build_trips_response(
        self,
        db: Session,
        trips: list[Trip]
    ) -> dict[str, Any]:
        """
        Build complete response with multiple trips and summary.
        
        Args:
            db: SQLAlchemy session
            trips: List of Trip ORM objects
        
        Returns:
            dict: Complete response data:
            {
                "trips": [...],
                "summary": {
                    "total_trips": 5,
                    "total_points": 1800,
                    "devices": ["ESP001", "ESP002"]
                }
            }
        
        Performance:
            - Processes trips sequentially (could parallelize in future)
            - Typical time: 50-200ms for 10 trips with 3000 total points
        
        Example:
            >>> trips = get_trips_in_time_range(db, start, end)
            >>> data = trip_assembler.build_trips_response(db, trips)
            >>> print(f"Found {data['summary']['total_trips']} trips")
        """
        if not trips:
            # Empty response
            return {
                "trips": [],
                "summary": {
                    "total_trips": 0,
                    "total_points": 0,
                    "devices": []
                }
            }
        
        # ========================================
        # Build trip JSONs
        # ========================================
        trip_jsons = []
        
        for trip in trips:
            try:
                trip_json = self.build_full_trip_json(db, trip)
                trip_jsons.append(trip_json)
            except Exception as e:
                # Log error but continue processing other trips
                trip_id = getattr(trip, 'trip_id', 'unknown')
                print(f"[TRIP_ASSEMBLER] Error building trip {trip_id}: {e}")
                continue
        
        # ========================================
        # Calculate summary statistics
        # ========================================
        total_trips = len(trip_jsons)
        total_points = sum(len(t['route']) for t in trip_jsons)
        
        # Extract unique device IDs
        devices_set = {t['device_id'] for t in trip_jsons}
        devices = sorted(list(devices_set))
        
        summary = {
            "total_trips": total_trips,
            "total_points": total_points,
            "devices": devices
        }
        
        # ========================================
        # Assemble final response
        # ========================================
        return {
            "trips": trip_jsons,
            "summary": summary
        }


# ==========================================================
# Singleton Instance
# ==========================================================
trip_assembler = TripAssembler()