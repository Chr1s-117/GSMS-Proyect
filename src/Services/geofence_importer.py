# src/Services/geofence_importer.py

"""
Geofence Import Service from GeoJSON Files

This service provides functionality to bulk import geofences from GeoJSON files
into the PostgreSQL/PostGIS database. It handles coordinate transformation,
geometry conversion, duplicate detection, and error recovery.

Key features:
- Reads GeoJSON files using GeoPandas
- Automatic CRS reprojection to WGS84 (EPSG:4326)
- Converts Shapely geometries to PostGIS WKT format
- Three import modes: skip, update, replace
- Batch validation and error handling
- Progress reporting and statistics
- Transaction rollback on errors

Import Modes:
- skip: Skip existing geofences (default, safest)
- update: Update existing geofences with new data
- replace: Delete and recreate existing geofences

Supported Geometry Types:
- Polygon (most common for geofences)
- MultiPolygon (for complex areas)
- Point (converted to buffered polygon)
- LineString (converted to buffered polygon)

File Format:
GeoJSON files must follow RFC 7946 standard with properties:
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": "warehouse-001",
                "name": "Main Warehouse",
                "description": "Primary storage facility",
                "type": "warehouse",
                "is_active": true,
                "color": "#28a745",
                "metadata": {"capacity": 5000}
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[lon, lat], ...]]
            }
        }
    ]
}

Dependencies:
- geopandas: Spatial data manipulation
- shapely: Geometry operations
- pyproj: Coordinate transformations
"""

from typing import Tuple, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from geoalchemy2.elements import WKTElement
import geopandas as gpd
from shapely.geometry import shape, Point, LineString, Polygon
from src.Schemas.geofence import GeofenceCreate, GeofenceUpdate
from src.Repositories.geofence import get_geofence_by_id, create_geofence, update_geofence, delete_geofence


class GeofenceImporter:
    """
    Service for importing geofences from GeoJSON files and GeoDataFrames.
    
    This class handles the complete import pipeline:
    1. File loading and validation
    2. Coordinate system transformation
    3. Geometry conversion (Shapely → PostGIS WKT)
    4. Duplicate detection and handling
    5. Database insertion with error recovery
    6. Statistics reporting
    
    Usage:
        importer = GeofenceImporter()
        created, updated, skipped, failed = importer.import_from_file(
            db, "geofences.geojson", mode="skip"
        )
        print(f"Import complete: {created} created, {updated} updated")
    """
    
    def import_from_file(
        self, 
        db: Session, 
        filepath: str,
        mode: str = 'skip',
        buffer_distance: float = 0.0
    ) -> Tuple[int, int, int, int]:
        """
        Import geofences from a GeoJSON file.
        
        This is the main entry point for file-based imports. It loads the
        GeoJSON file using GeoPandas and delegates to import_from_geodataframe().
        
        Args:
            db: SQLAlchemy session
            filepath: Path to GeoJSON file (absolute or relative)
            mode: Import mode - 'skip' | 'update' | 'replace'
                - 'skip': Skip existing geofences (default, safest)
                - 'update': Update existing geofences with new data
                - 'replace': Delete and recreate existing geofences
            buffer_distance: Buffer distance in meters for Point/LineString geometries
                             (default: 0.0 = no buffer, use actual geometry)
        
        Returns:
            Tuple of (created, updated, skipped, failed) counts
            
        Raises:
            FileNotFoundError: If GeoJSON file doesn't exist
            ValueError: If file format is invalid
            
        Example:
            created, updated, skipped, failed = importer.import_from_file(
                db, "/data/warehouses.geojson", mode="skip"
            )
            print(f"Created: {created}, Updated: {updated}, Skipped: {skipped}, Failed: {failed}")
        """
        print(f"[IMPORT] Loading geofences from: {filepath}")
        
        try:
            # Read GeoJSON file with geopandas
            gdf = gpd.read_file(filepath)
            print(f"[IMPORT] Loaded {len(gdf)} features from file")
            
        except FileNotFoundError:
            print(f"[IMPORT] ERROR: File not found: {filepath}")
            raise
        except Exception as e:
            print(f"[IMPORT] ERROR: Failed to read GeoJSON file: {e}")
            raise ValueError(f"Invalid GeoJSON file: {e}")
        
        return self.import_from_geodataframe(db, gdf, mode=mode, buffer_distance=buffer_distance)
    
    def import_from_geodataframe(
        self,
        db: Session,
        gdf: gpd.GeoDataFrame,
        mode: str = 'skip',
        buffer_distance: float = 0.0
    ) -> Tuple[int, int, int, int]:
        """
        Import geofences from a GeoDataFrame.
        
        This method processes a GeoDataFrame (loaded from file or created programmatically)
        and imports all features as geofences into the database.
        
        Processing pipeline:
        1. Validate and reproject CRS to EPSG:4326 (WGS84)
        2. Iterate through each feature
        3. Extract properties and geometry
        4. Convert geometry to PostGIS WKT format
        5. Check for existing geofence by ID
        6. Apply import mode logic (skip/update/replace)
        7. Insert or update in database
        8. Handle errors and rollback on failure
        
        Args:
            db: SQLAlchemy session
            gdf: GeoDataFrame containing geofence features
            mode: Import mode - 'skip' | 'update' | 'replace'
            buffer_distance: Buffer distance in meters for Point/LineString geometries
        
        Returns:
            Tuple of (created, updated, skipped, failed) counts
            
        Example:
            import geopandas as gpd
            gdf = gpd.read_file("warehouses.geojson")
            created, updated, skipped, failed = importer.import_from_geodataframe(
                db, gdf, mode="update"
            )
        """
        created = 0
        updated = 0
        skipped = 0
        failed = 0
        
        # ========================================
        # STEP 1: Validate and reproject CRS
        # ========================================
        if gdf.crs is None:
            print("[IMPORT] WARNING: No CRS defined, assuming EPSG:4326")
            gdf = gdf.set_crs('EPSG:4326')
        elif gdf.crs != 'EPSG:4326':
            print(f"[IMPORT] Reprojecting from {gdf.crs} to EPSG:4326 (WGS84)")
            gdf = gdf.to_crs('EPSG:4326')
        
        # ========================================
        # STEP 2: Process each feature
        # ========================================
        total_features = len(gdf)
        print(f"[IMPORT] Processing {total_features} features in mode '{mode}'...")
        
        for idx, row in gdf.iterrows():
            try:
                # Extract required ID field
                geofence_id = row.get('id')
                if not geofence_id:
                    print(f"[IMPORT] ERROR: Feature {idx} missing 'id' field - skipping")
                    failed += 1
                    continue
                
                geofence_id = str(geofence_id)
                
                # ========================================
                # STEP 3: Process geometry
                # ========================================
                geometry = row.geometry
                
                # Validate geometry
                if geometry is None or geometry.is_empty:
                    print(f"[IMPORT] ERROR: Feature {geofence_id} has empty geometry - skipping")
                    failed += 1
                    continue
                
                # Apply buffer to Point/LineString geometries if requested
                if buffer_distance > 0:
                    if isinstance(geometry, (Point, LineString)):
                        print(f"[IMPORT] Buffering {type(geometry).__name__} geometry by {buffer_distance}m")
                        # Buffer in meters (approximate, for exact use projected CRS)
                        geometry = geometry.buffer(buffer_distance / 111320)  # Rough conversion to degrees
                
                # Ensure geometry is Polygon or MultiPolygon
                if not isinstance(geometry, (Polygon, gpd.GeoDataFrame)):
                    print(f"[IMPORT] WARNING: Feature {geofence_id} has {type(geometry).__name__} geometry")
                
                # Convert to WKT for PostGIS
                geometry_wkt = geometry.wkt
                
                # ========================================
                # STEP 4: Extract properties
                # ========================================
                geofence_data = {
                    'id': geofence_id,
                    'name': row.get('name') or f'Geofence {geofence_id}',
                    'description': row.get('description'),
                    'type': row.get('type', 'custom'),
                    'is_active': bool(row.get('is_active', True)),
                    'color': row.get('color', '#3388ff'),
                    'geometry': WKTElement(geometry_wkt, srid=4326),
                    'extra_metadata': row.get('metadata')
                }
                
                # ========================================
                # STEP 5: Apply import mode logic
                # ========================================
                existing = get_geofence_by_id(db, geofence_id)
                
                if existing:
                    if mode == 'skip':
                        skipped += 1
                        print(f"[IMPORT] [{idx+1}/{total_features}] Skipped (exists): {geofence_id}")
                        continue
                    
                    elif mode == 'update':
                        # Update using Pydantic schema
                        update_schema = GeofenceUpdate(**{
                            k: v for k, v in geofence_data.items() 
                            if k != 'id'  # Exclude ID from update
                        })
                        update_geofence(db, geofence_id, update_schema)
                        updated += 1
                        print(f"[IMPORT] [{idx+1}/{total_features}] Updated: {geofence_id} - {geofence_data['name']}")
                    
                    elif mode == 'replace':
                        delete_geofence(db, geofence_id)
                        create_schema = GeofenceCreate(**geofence_data)
                        create_geofence(db, create_schema)
                        created += 1
                        print(f"[IMPORT] [{idx+1}/{total_features}] Replaced: {geofence_id} - {geofence_data['name']}")
                    
                    else:
                        print(f"[IMPORT] ERROR: Invalid mode '{mode}' - skipping")
                        failed += 1
                        continue
                
                else:
                    # Create new geofence using Pydantic schema
                    create_schema = GeofenceCreate(**geofence_data)
                    create_geofence(db, create_schema)
                    created += 1
                    print(f"[IMPORT] [{idx+1}/{total_features}] Created: {geofence_id} - {geofence_data['name']}")
            
            except IntegrityError as ie:
                db.rollback()
                failed += 1
                error_msg = str(ie.orig) if hasattr(ie, 'orig') else str(ie)
                print(f"[IMPORT] IntegrityError for '{row.get('id', 'unknown')}': {error_msg}")
            
            except Exception as e:
                db.rollback()
                failed += 1
                print(f"[IMPORT] Error importing '{row.get('id', 'unknown')}': {type(e).__name__}: {e}")
        
        # ========================================
        # STEP 6: Print summary
        # ========================================
        print("\n" + "="*60)
        print("[IMPORT] Import Summary:")
        print(f"  Total Features:  {total_features}")
        print(f"  ✅ Created:      {created}")
        print(f"  🔄 Updated:      {updated}")
        print(f"  ⏭️  Skipped:      {skipped}")
        print(f"  ❌ Failed:       {failed}")
        print("="*60 + "\n")
        
        return (created, updated, skipped, failed)
    
    def validate_geojson(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, list[str]]:
        """
        Validate GeoJSON data before import.
        
        Checks for:
        - Required 'id' field in all features
        - Valid geometries (not empty, not null)
        - Geometry types (Polygon/MultiPolygon preferred)
        - CRS compatibility
        
        Args:
            gdf: GeoDataFrame to validate
            
        Returns:
            Tuple of (is_valid, list of error messages)
            
        Example:
            is_valid, errors = importer.validate_geojson(gdf)
            if not is_valid:
                for error in errors:
                    print(f"Validation error: {error}")
        """
        errors = []
        
        # Check for 'id' field
        if 'id' not in gdf.columns:
            errors.append("Missing required 'id' field in properties")
        else:
            # Check for null/empty IDs
            null_ids = gdf['id'].isna().sum()
            if null_ids > 0:
                errors.append(f"{null_ids} features have null/empty 'id' values")
        
        # Check geometries
        if gdf.geometry.isna().any():
            null_geoms = gdf.geometry.isna().sum()
            errors.append(f"{null_geoms} features have null geometries")
        
        empty_geoms = gdf.geometry.apply(lambda g: g.is_empty if g else True).sum()
        if empty_geoms > 0:
            errors.append(f"{empty_geoms} features have empty geometries")
        
        # Check CRS
        if gdf.crs is None:
            errors.append("No CRS defined (will assume EPSG:4326)")
        
        return (len(errors) == 0, errors)
    
    def export_to_file(
        self,
        db: Session,
        filepath: str,
        active_only: bool = True
    ) -> int:
        """
        Export geofences from database to GeoJSON file.
        
        Useful for:
        - Backup before bulk updates
        - Sharing geofence data
        - Visualization in GIS software
        
        Args:
            db: SQLAlchemy session
            filepath: Output GeoJSON file path
            active_only: Export only active geofences (default: True)
            
        Returns:
            Number of geofences exported
            
        Example:
            count = importer.export_to_file(db, "backup.geojson", active_only=True)
            print(f"Exported {count} geofences")
        """
        from src.Repositories.geofence import get_all_geofences
        from geoalchemy2.shape import to_shape
        
        # Get geofences from database
        geofences = get_all_geofences(db, only_active=active_only)
        
        if not geofences:
            print("[EXPORT] No geofences to export")
            return 0
        
        # Convert to GeoDataFrame
        features = []
        for gf in geofences:
            # Convert PostGIS geometry to Shapely
            shapely_geom = to_shape(gf.geometry)
            
            features.append({
                'id': gf.id,
                'name': gf.name,
                'description': gf.description,
                'type': gf.type,
                'is_active': gf.is_active,
                'color': gf.color,
                'metadata': gf.extra_metadata,
                'geometry': shapely_geom
            })
        
        gdf = gpd.GeoDataFrame(features, crs='EPSG:4326')
        
        # Write to file
        gdf.to_file(filepath, driver='GeoJSON')
        print(f"[EXPORT] Exported {len(features)} geofences to {filepath}")
        
        return len(features)


# ==========================================================
# Global Singleton Instance
# ==========================================================
"""
Singleton instance for global access across the application.

Usage:
    from src.Services.geofence_importer import geofence_importer
    
    created, updated, skipped, failed = geofence_importer.import_from_file(
        db, "geofences.geojson", mode="skip"
    )
"""
geofence_importer = GeofenceImporter()