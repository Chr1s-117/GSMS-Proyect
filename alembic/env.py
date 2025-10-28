# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv
from src.DB.base_class import Base
from src.Models.gps_data import GPS_data
from src.Models.device import Device
from src.Models.geofence import Geofence  
from src.Models.accelerometer_data import AccelerometerData
from sqlalchemy import MetaData
import geoalchemy2  # Asegura que GeoAlchemy2 esté importado para las migraciones

_ = GPS_data.__table__
_ = Device.__table__  
_ = Geofence.__table__  
_ = AccelerometerData.__table__
"""
load environment variables from .env file
"""
load_dotenv()

config = context.config

"""
This is the Alembic Config object, which provides
access to the values within the .ini file in use.
"""
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment variables")

config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ignorar tablas del sistema PostGIS
def include_object(object, name, type_, reflected, compare_to):
    """
    Ignora tablas del sistema PostGIS para evitar que Alembic las borre.
    """
    if type_ == "table":
        postgis_tables = [
            'spatial_ref_sys', 'geometry_columns', 'geography_columns',
            'raster_columns', 'raster_overviews', 'topology', 'layer',
            # Tiger Geocoder tables
            'loader_lookuptables', 'loader_platform', 'loader_variables',
            'addr', 'addrfeat', 'bg', 'county', 'county_lookup', 'countysub_lookup',
            'cousub', 'direction_lookup', 'edges', 'faces', 'featnames',
            'geocode_settings', 'geocode_settings_default', 'pagc_gaz', 'pagc_lex',
            'pagc_rules', 'place', 'place_lookup', 'secondary_unit_lookup',
            'state', 'state_lookup', 'street_type_lookup', 'tabblock', 'tabblock20',
            'tract', 'zcta5', 'zip_lookup', 'zip_lookup_all', 'zip_lookup_base',
            'zip_state', 'zip_state_loc'
        ]
        if name.lower() in postgis_tables:
            return False
    return True


target_metadata = Base.metadata


# ====================================================
# 🔧 Hook process_revision_directives (GeoAlchemy2 + DEBUG corregido)
# ====================================================
def process_revision_directives(context, revision, directives):
    """
    Hook de lifecycle que modifica las migraciones generadas automáticamente.
    
    1. Agrega automáticamente los imports necesarios para GeoAlchemy2
    2. Elimina operaciones de creación de índices espaciales duplicados (anidados también)
    """
    from alembic.operations import ops
    
    if directives:
        script = directives[0]
        
        if script.upgrade_ops is not None:
            uses_geoalchemy = False
            
            # Inspeccionar todas las operaciones del upgrade
            for i, op in enumerate(script.upgrade_ops.ops):
                print(f"🔍 [DEBUG] Operación {i}: {type(op).__name__}")
                
                # Buscar operaciones de creación de tabla con tipos espaciales
                if isinstance(op, ops.CreateTableOp):
                    for column in op.columns:
                        # Usar getattr para acceso seguro
                        col_type = getattr(column, 'type', None)
                        if col_type is None:
                            continue
                            
                        type_str = str(type(col_type))
                        
                        if ('Geography' in type_str or 'Geometry' in type_str):
                            uses_geoalchemy = True
                            col_name = getattr(column, 'key', getattr(column, 'name', 'unknown'))
                            table_name = getattr(op, 'table_name', 'unknown_table')
                            print(f"🔧 [PROCESS] Detectado tipo espacial en columna '{col_name}' de tabla '{table_name}'")
                
                # Buscar operaciones de creación de índices en primer nivel
                if isinstance(op, ops.CreateIndexOp):
                    kw = getattr(op, 'kw', {})
                    if kw.get('postgresql_using') == 'gist':
                        columns = getattr(op, 'columns', [])
                        if columns:
                            column_names = [str(col) for col in columns]
                            if any('geometry' in col_name.lower() for col_name in column_names):
                                index_name = getattr(op, 'index_name', 'unknown_index')
                                print(f"⚠️  [PROCESS] Encontrado índice espacial en nivel superior: {index_name}")
                
                # Buscar dentro de ModifyTableOps (operaciones anidadas)
                if isinstance(op, ops.ModifyTableOps):
                    sub_ops = getattr(op, 'ops', [])
                    if not sub_ops:
                        continue
                        
                    print(f"   🔎 [DEBUG] ModifyTableOps tiene {len(sub_ops)} sub-operaciones")
                    indices_to_remove = []
                    
                    for j, sub_op in enumerate(sub_ops):
                        print(f"      - Sub-op {j}: {type(sub_op).__name__}")
                        
                        if isinstance(sub_op, ops.CreateIndexOp):
                            index_name = getattr(sub_op, 'index_name', 'unknown_index')
                            table_name = getattr(sub_op, 'table_name', 'unknown_table')
                            
                            print(f"        📍 Índice encontrado: {index_name}")
                            print(f"           Tabla: {table_name}")
                            
                            columns = getattr(sub_op, 'columns', None)
                            if columns:
                                print(f"           Columnas: {columns}")
                            
                            kw = getattr(sub_op, 'kw', {})
                            print(f"           kw: {kw}")
                            
                            # Verificar si es índice espacial GIST
                            if kw.get('postgresql_using') == 'gist':
                                if columns:
                                    column_names = [str(col) for col in columns]
                                    if any('geometry' in col_name.lower() for col_name in column_names):
                                        indices_to_remove.append(j)
                                        print(f"⚠️  [PROCESS] Marcando índice espacial anidado '{index_name}' para eliminación")
                    
                    # Eliminar índices espaciales de las sub-operaciones
                    if indices_to_remove:
                        print(f"🗑️  [PROCESS] Eliminando {len(indices_to_remove)} índices espaciales anidados...")
                        for j in reversed(indices_to_remove):
                            removed_name = getattr(sub_ops[j], 'index_name', 'unknown_index')
                            sub_ops.pop(j)
                            print(f"✅ [PROCESS] Eliminado create_index anidado: {removed_name}")
            
            # Agregar imports de GeoAlchemy2 si es necesario
            if uses_geoalchemy:
                print("✅ [PROCESS] Agregando imports de GeoAlchemy2...")
                
                if script.imports is None:
                    script.imports = set()
                
                script.imports.add("import geoalchemy2")
                script.imports.add("from geoalchemy2 import Geography, Geometry")
                
                print("✅ [PROCESS] Imports agregados")


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,
        render_as_batch=False,
        process_revision_directives=process_revision_directives,  # ← AGREGADO
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True,
            render_as_batch=False,
            process_revision_directives=process_revision_directives,  # ← AGREGADO
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
