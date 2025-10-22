# src/Services/geofence_detector.py

"""
Geofence Detection Service

This service encapsulates the logic for determining if a GPS point is inside,
entering, or exiting geofences. It maintains state awareness by comparing
current GPS position with previous position to detect transitions.

Key features:
- Real-time point-in-polygon detection using PostGIS spatial queries
- Event detection (entry, exit, inside) based on state transitions
- Handles multiple overlapping geofences (returns most specific/smallest area)
- Optimized queries using spatial indexes
- Thread-safe singleton pattern

Event Types:
- entry: GPS enters a geofence (was outside or in different geofence)
- exit: GPS leaves a geofence (now outside all geofences)
- inside: GPS remains in the same geofence (no state change)
- None: GPS remains outside all geofences (no state change)

State Transition Matrix:
    Previous → Current     | Event Type
    ----------------------|------------
    None → Geofence A      | entry
    Geofence A → None      | exit
    Geofence A → Geofence A| inside
    Geofence A → Geofence B| entry (EXIT for A handled in UDP)
    None → None            | None (no event)
"""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.Repositories.gps_data import get_last_gps_row_by_device
from src.Models.geofence import Geofence


class GeofenceDetector:
    """
    Service for detecting geofence entry/exit/inside events.
    
    This class provides methods to:
    1. Check if a GPS point is inside any active geofence
    2. Detect state transitions (entry/exit/inside)
    3. Handle overlapping geofences (selects smallest area)
    
    Usage:
        detector = GeofenceDetector()
        event = detector.check_point(db, "TRUCK-001", 10.9878, -74.7889, timestamp)
        
        if event:
            print(f"Event: {event['event_type']} in {event['name']}")
    """

    def check_point(
        self,
        db: Session,
        device_id: str,
        lat: float,
        lon: float,
        timestamp: datetime
    ) -> Optional[Dict[str, Any]]:
        """
        Verify if a GPS point is inside a geofence and detect state transitions.
        
        This is the main entry point for geofence detection. It compares
        the current GPS position with the previous position to detect
        entry/exit/inside events.
        
        Args:
            db: SQLAlchemy session
            device_id: Unique identifier of the GPS device
            lat: GPS latitude (-90 to 90)
            lon: GPS longitude (-180 to 180)
            timestamp: UTC timestamp of the GPS reading
            
        Returns:
            Dictionary with geofence event information, or None if no event:
            {
                "id": "warehouse-001",           # Geofence ID (None for exit events)
                "name": "Main Warehouse",        # Geofence name (None for exit events)
                "event_type": "entry" | "exit" | "inside"
            }
            
        State transition logic:
            - Previous: None,        Current: Geofence A  → entry
            - Previous: Geofence A,  Current: None        → exit
            - Previous: Geofence A,  Current: Geofence A  → inside
            - Previous: Geofence A,  Current: Geofence B  → entry (EXIT handled externally)
            - Previous: None,        Current: None        → None (no event)
        
        Example:
            event = detector.check_point(db, "TRUCK-001", 10.9878, -74.7889, now)
            
            # Entry event
            # {"id": "warehouse-001", "name": "Main Warehouse", "event_type": "entry"}
            
            # Exit event
            # {"id": None, "name": None, "event_type": "exit"}
            
            # Inside (no state change)
            # {"id": "warehouse-001", "name": "Main Warehouse", "event_type": "inside"}
            
            # Outside (no event)
            # None
        """

        # ========================================
        # STEP 1: Find current geofence (if any)
        # ========================================
        current_geofence = self._find_containing_geofence(db, lat, lon)

        # ========================================
        # STEP 2: Get previous GPS to detect transitions
        # ========================================
        previous_gps = get_last_gps_row_by_device(db, device_id)
        previous_geofence_id = (
            previous_gps.get('CurrentGeofenceID') if previous_gps else None
        )

        # ========================================
        # STEP 3: State transition matrix
        # ========================================
        if current_geofence:
            current_id = current_geofence['id']

            if current_id != previous_geofence_id:
                # State change detected: entering new geofence
                # (or transitioning from one geofence to another)
                return {
                    'id': current_id,
                    'name': current_geofence['name'],
                    'event_type': 'entry'
                }
            else:
                # No state change: still inside same geofence
                return {
                    'id': current_id,
                    'name': current_geofence['name'],
                    'event_type': 'inside'
                }

        else:
            # GPS is outside all geofences
            if previous_geofence_id:
                # State change: was inside, now outside → EXIT event
                return {
                    'id': None,
                    'name': None,
                    'event_type': 'exit'
                }
            else:
                # No state change: was outside, still outside → no event
                return None

    def _find_containing_geofence(
        self,
        db: Session,
        lat: float,
        lon: float
    ) -> Optional[Dict[str, str]]:
        """
        Find if a GPS point is contained within any active geofence.
        
        Uses PostGIS spatial query with the following optimizations:
        - Only checks active geofences (is_active = TRUE)
        - Uses spatial index (GIST) for fast lookup
        - Returns smallest geofence (by area) if multiple overlap
        
        IMPORTANT: PostGIS Geography type uses ST_Intersects instead of ST_Contains
        because Geography is spherical and ST_Contains has limitations with it.
        ST_Intersects effectively does point-in-polygon check for our use case.
        
        Args:
            db: SQLAlchemy session
            lat: GPS latitude (-90 to 90)
            lon: GPS longitude (-180 to 180)
            
        Returns:
            Dictionary with geofence id and name, or None if outside all geofences:
            {"id": "warehouse-001", "name": "Main Warehouse"}
        
        Query explanation:
            - ST_GeogFromText creates a Geography POINT from WKT
            - ST_Intersects checks if point intersects with geofence polygon
            - ST_Area calculates spherical area (for sorting by smallest)
            - ORDER BY area ASC ensures most specific geofence is returned
            - LIMIT 1 returns only the smallest matching geofence
        
        Performance:
            - Uses idx_geofences_geometry spatial index (GIST)
            - Typical query time: <5ms for 100+ geofences
        """

        # Raw SQL query using PostGIS functions
        # Note: We use text() for parameterized queries with named parameters
        query = text("""
            SELECT id, name, ST_Area(geometry) AS area
            FROM geofences
            WHERE is_active = TRUE
            AND ST_Intersects(
                geometry,
                ST_GeogFromText('POINT(' || :lon || ' ' || :lat || ')')
            )
            ORDER BY area ASC
            LIMIT 1
        """)

        try:
            result = db.execute(query, {'lon': lon, 'lat': lat}).first()

            if result:
                return {
                    'id': str(result.id),   # Ensure string type
                    'name': str(result.name)
                }
            return None
            
        except Exception as e:
            # Log error but don't crash - return None to indicate no geofence
            print(f"[GEOFENCE] Error in _find_containing_geofence: {e}")
            return None

    def _get_geofence_by_id(
        self, 
        db: Session, 
        geofence_id: str
    ) -> Optional[Dict[str, str]]:
        """
        Retrieve basic geofence information by ID.
        
        Used internally when we need to fetch geofence metadata
        (e.g., for exit events where we want to log the geofence name).
        
        Args:
            db: SQLAlchemy session
            geofence_id: Unique geofence identifier
            
        Returns:
            Dictionary with geofence id and name, or None if not found:
            {"id": "warehouse-001", "name": "Main Warehouse"}
        
        Example:
            info = detector._get_geofence_by_id(db, "warehouse-001")
            # {"id": "warehouse-001", "name": "Main Warehouse"}
        """
        try:
            geofence = db.query(Geofence).filter(
                Geofence.id == geofence_id
            ).first()
            
            if geofence:
                return {
                    'id': str(geofence.id),
                    'name': str(geofence.name)
                }
            return None
            
        except Exception as e:
            print(f"[GEOFENCE] Error in _get_geofence_by_id: {e}")
            return None

    def get_all_containing_geofences(
        self,
        db: Session,
        lat: float,
        lon: float
    ) -> list[Dict[str, str]]:
        """
        Get ALL geofences that contain a GPS point (for overlapping geofences).
        
        Unlike _find_containing_geofence which returns only the smallest,
        this method returns all overlapping geofences sorted by area.
        
        Useful for:
        - Analytics (track all zones a device is in)
        - Complex business rules (check multiple zone types)
        - Debugging overlapping geofences
        
        Args:
            db: SQLAlchemy session
            lat: GPS latitude (-90 to 90)
            lon: GPS longitude (-180 to 180)
            
        Returns:
            List of geofence dictionaries (empty list if outside all):
            [
                {"id": "warehouse-001", "name": "Main Warehouse", "type": "warehouse"},
                {"id": "industrial-zone-1", "name": "Industrial Zone", "type": "zone"}
            ]
        
        Example:
            geofences = detector.get_all_containing_geofences(db, 10.9878, -74.7889)
            for gf in geofences:
                print(f"Inside: {gf['name']} ({gf['type']})")
        """
        query = text("""
            SELECT id, name, type, ST_Area(geometry) AS area
            FROM geofences
            WHERE is_active = TRUE
            AND ST_Intersects(
                geometry,
                ST_GeogFromText('POINT(' || :lon || ' ' || :lat || ')')
            )
            ORDER BY area ASC
        """)

        try:
            results = db.execute(query, {'lon': lon, 'lat': lat}).fetchall()

            return [
                {
                    'id': str(row.id),
                    'name': str(row.name),
                    'type': str(row.type) if hasattr(row, 'type') else 'custom'
                }
                for row in results
            ]
            
        except Exception as e:
            print(f"[GEOFENCE] Error in get_all_containing_geofences: {e}")
            return []


# ==========================================================
# Global Singleton Instance
# ==========================================================
"""
Singleton instance for global access across the application.

Usage:
    from src.Services.geofence_detector import geofence_detector
    
    event = geofence_detector.check_point(db, device_id, lat, lon, timestamp)
"""
geofence_detector = GeofenceDetector()