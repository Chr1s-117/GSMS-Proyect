# src/Services/geofence_importer.py

"""
Servicio de importación de geocercas desde archivos GeoJSON normalizados.

IMPORTANTE: Los archivos GeoJSON deben estar previamente en EPSG:4326.
Para archivos en otros CRS, normalízalos primero con el script de preparación.

Funcionalidad:
- Lee archivos GeoJSON (sin geopandas)
- Convierte geometrías a formato PostGIS WKT usando Shapely
- Importa a PostgreSQL con manejo de duplicados
"""

from typing import Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
from shapely.geometry import shape
from src.Repositories.geofence import get_geofence_by_id, create_geofence, update_geofence


class GeofenceImporter:
    """
    Importador de geocercas desde GeoJSON.
    """

    def import_from_file(
        self,
        db: Session,
        filepath: str,
        mode: str = 'skip'
    ) -> Tuple[int, int, int, int]:
        """
        Importa geocercas desde archivo GeoJSON local.
        
        Args:
            db: Session SQLAlchemy
            filepath: Ruta al archivo GeoJSON (DEBE estar en EPSG:4326)
            mode: Modo de importación
                - 'skip': Salta duplicados (default)
                - 'update': Actualiza duplicados
                - 'replace': Reemplaza todos
        
        Returns:
            Tupla (created, updated, skipped, failed)
        
        Note:
            Este método asume que el GeoJSON está normalizado a EPSG:4326.
            Features sin 'id' o sin geometría serán contados como 'skipped'.
            Geometrías inválidas se intentan reparar con buffer(0).
        """
        print(f"[IMPORT] Loading geofences from: {filepath}")

        # Leer archivo GeoJSON
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
        except FileNotFoundError:
            print(f"[IMPORT] File not found: {filepath}")
            return (0, 0, 0, 0)
        except json.JSONDecodeError as e:
            print(f"[IMPORT] Invalid JSON format: {e}")
            return (0, 0, 0, 0)

        # Validar estructura básica
        if geojson_data.get('type') != 'FeatureCollection':
            print("[IMPORT] Invalid GeoJSON: expected 'FeatureCollection'")
            return (0, 0, 0, 0)

        # ✅ Validación adicional de CRS
        crs = geojson_data.get('crs', {}).get('properties', {}).get('name', '')
        if crs and 'EPSG:4326' not in crs and 'WGS84' not in crs:
            print(f"[IMPORT] Warning: CRS is {crs}, expected EPSG:4326")

        features = geojson_data.get('features', [])
        print(f"[IMPORT] Loaded {len(features)} geofences from file")
        print("[IMPORT] Assuming GeoJSON is in EPSG:4326")

        return self.import_from_geojson_dict(db, geojson_data, mode=mode)

    def import_from_geojson_dict(
        self,
        db: Session,
        geojson_dict: dict,
        mode: str = 'skip'
    ) -> Tuple[int, int, int, int]:
        """
        Importa geocercas desde un diccionario GeoJSON.

        Args:
            db: Session SQLAlchemy
            geojson_dict: Diccionario con formato GeoJSON
            mode: 'skip' | 'update' | 'replace'

        Returns:
            (created, updated, skipped, failed)
        """
        created = 0
        updated = 0
        skipped = 0
        failed = 0

        features = geojson_dict.get('features', [])

        for feature in features:
            properties = {}  # inicialización temprana
            try:
                properties = feature.get('properties', {})
                geometry_dict = feature.get('geometry')

                if not geometry_dict:
                    print("[IMPORT] Skipping feature without geometry")
                    skipped += 1
                    continue

                geofence_id = str(properties.get('id') or feature.get('id') or '').strip()
                if not geofence_id:
                    print("[IMPORT] Warning: Feature without ID, skipping")
                    skipped += 1
                    continue

                # Convertir geometría a WKT
                try:
                    geom = shape(geometry_dict)
                    geom_type = geom.geom_type  # ✅ Tipo de geometría en el log
                    if not geom.is_valid:
                        geom = geom.buffer(0)
                    geometry_wkt = geom.wkt
                except Exception as e:
                    print(f"[IMPORT] Invalid geometry for {geofence_id}: {e}")
                    failed += 1
                    continue

                # Preparar datos para insert/update
                geofence_data = {
                    'id': geofence_id,
                    'name': properties.get('name') or f'Geofence {geofence_id}',
                    'description': properties.get('description'),
                    'type': properties.get('type', 'custom'),
                    'is_active': properties.get('is_active', True),
                    'color': properties.get('color', '#3388ff'),
                    'geometry': geometry_wkt,
                    'extra_metadata': properties.get('metadata')
                }

                # Verificar si ya existe
                existing = get_geofence_by_id(db, geofence_id)

                if existing:
                    if mode == 'skip':
                        skipped += 1
                        print(f"[IMPORT] Skipped (exists): {geofence_id}")
                        continue

                    elif mode == 'update':
                        update_geofence(db, geofence_id, geofence_data)
                        updated += 1
                        print(f"[IMPORT] Updated: {geofence_id}")

                    elif mode == 'replace':
                        db.delete(existing)
                        db.commit()
                        create_geofence(db, geofence_data)
                        created += 1
                        print(f"[IMPORT] Replaced: {geofence_id} ({geom_type})")

                else:
                    create_geofence(db, geofence_data)
                    created += 1
                    print(f"[IMPORT] Created {geom_type}: {geofence_id}")

            except IntegrityError as ie:
                db.rollback()
                failed += 1
                print(f"[IMPORT] IntegrityError for {properties.get('id', 'unknown')}: {ie}")

            except Exception as e:
                db.rollback()
                failed += 1
                print(f"[IMPORT] Error importing {properties.get('id', 'unknown')}: {e}")

        print(f"[IMPORT] Processed: {created} created, {updated} updated, "
              f"{skipped} skipped, {failed} failed")

        return (created, updated, skipped, failed)


# Singleton
geofence_importer = GeofenceImporter()
