# src/Services/geofence_importer.py
"""
Geofence Importer Service
Imports geofences from GeoJSON files into PostgreSQL/PostGIS

Version: 2025-10-27
Author: Chr1s-117
Changes: Removed GeoPandas dependency, uses pure Shapely + JSON
"""

import json
import logging
from pathlib import Path
from typing import Tuple, Optional
from shapely.geometry import shape, mapping
from shapely import wkt as shapely_wkt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.Models.geofence import Geofence

# ============================================
# Module-level logging
# ============================================
logger = logging.getLogger(__name__)


class GeofenceImporter:
    """
    Imports geofence data from GeoJSON files into PostgreSQL/PostGIS.
    
    Uses Shapely for geometry handling instead of GeoPandas to avoid GDAL dependency.
    """

    def __init__(self, db: Session):
        """
        Initialize the geofence importer.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def import_from_file(
        self, 
        file_path: str,
        default_type: str = "polygon"
    ) -> Tuple[int, int, int, int]:
        """
        Import geofences from a GeoJSON file.
        
        Args:
            file_path: Path to the GeoJSON file
            default_type: Default geofence type if not specified in properties
        
        Returns:
            Tuple of (created, updated, skipped, failed) counts
        """
        created = 0
        updated = 0
        skipped = 0
        failed = 0

        try:
            # Read GeoJSON file
            file_path_obj = Path(file_path)
            
            if not file_path_obj.exists():
                print(f"[GEOFENCE-IMPORTER] ❌ File not found: {file_path}")
                return (0, 0, 0, 1)

            print(f"[GEOFENCE-IMPORTER] 📂 Reading file: {file_path}")
            
            with open(file_path_obj, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)

            # Extract features
            features = geojson_data.get('features', [])
            
            if not features:
                print("[GEOFENCE-IMPORTER] ⚠️  No features found in GeoJSON")
                return (0, 0, 0, 0)

            print(f"[GEOFENCE-IMPORTER] 📊 Processing {len(features)} features...")

            # Process each feature
            for idx, feature in enumerate(features):
                try:
                    # Extract properties and geometry
                    properties = feature.get('properties', {})
                    geometry = feature.get('geometry')

                    if not geometry:
                        print(f"[GEOFENCE-IMPORTER] ⚠️  Feature {idx} has no geometry, skipping")
                        skipped += 1
                        continue

                    # Convert GeoJSON geometry to Shapely object
                    try:
                        geom = shape(geometry)
                    except Exception as e:
                        print(f"[GEOFENCE-IMPORTER] ❌ Invalid geometry in feature {idx}: {e}")
                        failed += 1
                        continue

                    # Validate geometry
                    if not geom.is_valid:
                        print(f"[GEOFENCE-IMPORTER] ⚠️  Invalid geometry in feature {idx}, attempting to fix...")
                        geom = geom.buffer(0)  # Attempt to fix invalid geometry
                        
                        if not geom.is_valid:
                            print(f"[GEOFENCE-IMPORTER] ❌ Could not fix geometry in feature {idx}")
                            failed += 1
                            continue

                    # Convert to WKT for PostGIS
                    wkt = geom.wkt

                    # Extract properties
                    name = properties.get('name') or properties.get('NAME') or f"Geofence_{idx}"
                    geofence_type = properties.get('type') or properties.get('TYPE') or default_type
                    description = properties.get('description') or properties.get('DESCRIPTION')
                    
                    # Check if geofence already exists
                    existing = self.db.query(Geofence).filter_by(name=name).first()

                    if existing:
                        # Update existing geofence
                        existing.geometry = f"SRID=4326;{wkt}"
                        existing.type = geofence_type  # ✅ CORREGIDO: type (no geofence_type)
                        
                        if description:
                            existing.description = description
                        
                        updated += 1
                        print(f"[GEOFENCE-IMPORTER] ♻️  Updated: {name}")
                    else:
                        # Create new geofence
                        new_geofence = Geofence(
                            name=name,
                            geometry=f"SRID=4326;{wkt}",
                            type=geofence_type,  # ✅ CORREGIDO: type (no geofence_type)
                            description=description
                        )
                        self.db.add(new_geofence)
                        created += 1
                        print(f"[GEOFENCE-IMPORTER] ✅ Created: {name}")

                except Exception as e:
                    print(f"[GEOFENCE-IMPORTER] ❌ Error processing feature {idx}: {e}")
                    failed += 1
                    continue

            # Commit all changes
            try:
                self.db.commit()
                print(f"[GEOFENCE-IMPORTER] 💾 Database commit successful")
            except SQLAlchemyError as e:
                print(f"[GEOFENCE-IMPORTER] ❌ Database commit failed: {e}")
                self.db.rollback()
                # If commit fails, all are considered failed
                return (0, 0, 0, created + updated)

            # Print summary
            print(f"[GEOFENCE-IMPORTER] 📊 Import Summary:")
            print(f"  ✅ Created: {created}")
            print(f"  ♻️  Updated: {updated}")
            print(f"  ⏭️  Skipped: {skipped}")
            print(f"  ❌ Failed:  {failed}")

        except Exception as e:
            print(f"[GEOFENCE-IMPORTER] ❌ Fatal error: {e}")
            self.db.rollback()
            return (0, 0, 0, len(features) if 'features' in locals() else 1)

        return (created, updated, skipped, failed)

    def export_to_geojson(
        self, 
        output_path: str,
        geofence_type: Optional[str] = None
    ) -> bool:
        """
        Export geofences from database to GeoJSON file.
        
        Args:
            output_path: Path where to save the GeoJSON file
            geofence_type: Optional filter by geofence type
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Query geofences
            query = self.db.query(Geofence)
            
            if geofence_type:
                query = query.filter_by(type=geofence_type)  # ✅ CORREGIDO: type
            
            geofences = query.all()

            if not geofences:
                print("[GEOFENCE-IMPORTER] ⚠️  No geofences found to export")
                return False

            # Build GeoJSON structure
            features = []
            
            for geofence in geofences:
                try:
                    # Extract WKT and remove SRID prefix
                    wkt_str = str(geofence.geometry)
                    if wkt_str.startswith('SRID='):
                        wkt_str = wkt_str.split(';', 1)[1]
                    
                    # Convert WKT to Shapely geometry
                    geom = shapely_wkt.loads(wkt_str)
                    
                    # Convert to GeoJSON geometry
                    geom_json = mapping(geom)
                    
                    # Build feature
                    feature = {
                        "type": "Feature",
                        "properties": {
                            "id": geofence.id,
                            "name": geofence.name,
                            "type": geofence.type,  # ✅ CORREGIDO: type
                            "description": geofence.description,
                            "created_at": geofence.created_at.isoformat() if geofence.created_at else None,
                            "updated_at": geofence.updated_at.isoformat() if geofence.updated_at else None
                        },
                        "geometry": geom_json
                    }
                    
                    features.append(feature)
                    
                except Exception as e:
                    print(f"[GEOFENCE-IMPORTER] ⚠️  Error exporting geofence {geofence.name}: {e}")
                    continue

            # Build complete GeoJSON
            geojson = {
                "type": "FeatureCollection",
                "features": features
            }

            # Write to file
            output_path_obj = Path(output_path)
            output_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path_obj, 'w', encoding='utf-8') as f:
                json.dump(geojson, f, indent=2, ensure_ascii=False)

            print(f"[GEOFENCE-IMPORTER] ✅ Exported {len(features)} geofences to {output_path}")
            return True

        except Exception as e:
            print(f"[GEOFENCE-IMPORTER] ❌ Export failed: {e}")
            return False


# ============================================
# Global instance for backward compatibility
# ============================================
geofence_importer = None


def init_geofence_importer(db: Session):
    """
    Initialize the global geofence_importer instance.
    
    Args:
        db: SQLAlchemy database session
    
    Returns:
        GeofenceImporter instance
    """
    global geofence_importer
    geofence_importer = GeofenceImporter(db)
    logger.info("[GEOFENCE-IMPORTER] ✅ Global instance initialized")
    return geofence_importer