# src/Services/geofence_importer.py
import json
from pathlib import Path
from typing import Tuple
from shapely.geometry import shape
from sqlalchemy.orm import Session
from src.Models.geofence import Geofence

class GeofenceImporter:
    def __init__(self, db: Session):
        self.db = db

    def import_from_file(self, file_path: str) -> Tuple[int, int, int, int]:
        """
        Importa geofences desde un archivo GeoJSON.
        Returns: (created, updated, skipped, failed)
        """
        created = 0
        updated = 0
        skipped = 0
        failed = 0

        try:
            # Leer GeoJSON directamente (sin GeoPandas)
            with open(file_path, 'r', encoding='utf-8') as f:
                geojson = json.load(f)

            features = geojson.get('features', [])
            
            for feature in features:
                try:
                    properties = feature.get('properties', {})
                    geometry = feature.get('geometry')

                    # Convertir a Shapely geometry
                    geom = shape(geometry)
                    wkt = geom.wkt

                    # Extraer propiedades
                    name = properties.get('name', 'Unknown')
                    geofence_type = properties.get('type', 'polygon')
                    
                    # Buscar si ya existe
                    existing = self.db.query(Geofence).filter_by(name=name).first()

                    if existing:
                        # Actualizar
                        existing.geometry = f"SRID=4326;{wkt}"
                        existing.geofence_type = geofence_type
                        updated += 1
                    else:
                        # Crear nuevo
                        new_geofence = Geofence(
                            name=name,
                            geometry=f"SRID=4326;{wkt}",
                            geofence_type=geofence_type
                        )
                        self.db.add(new_geofence)
                        created += 1

                except Exception as e:
                    print(f"[GEOFENCE-IMPORTER] Error processing feature: {e}")
                    failed += 1
                    continue

            # Commit al final
            self.db.commit()
            print(f"[GEOFENCE-IMPORTER] Import complete: {created} created, {updated} updated, {failed} failed")

        except Exception as e:
            print(f"[GEOFENCE-IMPORTER] Fatal error: {e}")
            self.db.rollback()
            failed += 1

        return (created, updated, skipped, failed)