# alembic/env.py

"""
Alembic Environment Configuration for GSMS

This script configures the Alembic migration environment for both
"offline" (SQL script generation) and "online" (direct execution) modes.

Key Features:
- Loads DATABASE_URL from environment variables (not .env in production)
- Imports all SQLAlchemy models for autogeneration
- Filters PostGIS system tables to prevent accidental deletion
- Handles GeoAlchemy2 spatial types and indexes correctly

Environment Compatibility:
- Local Development: DATABASE_URL from .env file (via load_dotenv)
- AWS Production: DATABASE_URL from systemd environment (/etc/gsms/env)

Migration Workflow:
1. Modify models in src/Models/
2. Generate migration: alembic revision --autogenerate -m "Description"
3. Review generated migration in alembic/versions/
4. Apply migration: alembic upgrade head

PostGIS Requirements:
- PostgreSQL must have PostGIS extension enabled
- Extension is created automatically in first migration
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

# ============================================================
# Environment Variable Loading
# ============================================================

# For local development: load .env file
# For AWS production: this is a no-op (env vars injected by systemd)
try:
    from dotenv import load_dotenv
    load_dotenv()
    # Note: In AWS, load_dotenv() does nothing since .env doesn't exist
    # This is intentional and safe - env vars come from /etc/gsms/env
except ImportError:
    # dotenv not installed (acceptable in production)
    pass

# Alternative: Read from settings directly (more explicit)
# This ensures consistency with session.py and config.py
try:
    from src.Core.config import settings
    DATABASE_URL = settings.DATABASE_URL
except ImportError:
    # Fallback to environment variable if settings import fails
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set. "
        "Set it in .env (local) or export it as environment variable (AWS)."
    )

# ============================================================
# Alembic Configuration
# ============================================================

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configure Python logging using alembic.ini if available
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ============================================================
# Import All Models (Required for Autogeneration)
# ============================================================

"""
CRITICAL: All models must be imported here for Alembic to detect them.
If a model is not imported, it will NOT be included in migrations.

Current Models:
- GPS_data: GPS tracking records with geofence association
- Device: Registered GPS devices
- Geofence: Geographic boundaries with PostGIS geometry
"""

from src.DB.base_class import Base
from src.Models.gps_data import GPS_data
from src.Models.device import Device
from src.Models.geofence import Geofence

# Ensure GeoAlchemy2 is available for spatial types
import geoalchemy2

# Force table loading by referencing __table__
_ = GPS_data.__table__
_ = Device.__table__
_ = Geofence.__table__

# Set target metadata for Alembic autogeneration
target_metadata = Base.metadata

# ============================================================
# PostGIS Table Filter (CRITICAL)
# ============================================================

def include_object(object, name, type_, reflected, compare_to):
    """
    Filter function to exclude PostGIS system tables from Alembic operations.
    
    Without this filter, Alembic would attempt to drop PostGIS system tables
    during migrations, breaking PostGIS functionality.
    
    Args:
        object: SQLAlchemy object being processed
        name: Name of the table/column/index
        type_: Type of object ('table', 'column', 'index', etc.)
        reflected: Whether object was reflected from database
        compare_to: Object being compared to (for upgrades)
    
    Returns:
        bool: True if object should be processed, False to ignore
    
    Excluded PostGIS Tables:
    - spatial_ref_sys: Spatial reference system definitions
    - geometry_columns: PostGIS geometry column registry
    - geography_columns: PostGIS geography column registry
    - raster_*: Raster data support tables
    - topology: Topology extension tables
    - Tiger Geocoder tables: US address normalization tables
    """
    if type_ == "table":
        postgis_tables = [
            # Core PostGIS tables
            'spatial_ref_sys', 'geometry_columns', 'geography_columns',
            'raster_columns', 'raster_overviews', 'topology', 'layer',
            
            # Tiger Geocoder tables (US address normalization)
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
            return False  # Exclude this table
    
    return True  # Include all other objects


# ============================================================
# GeoAlchemy2 Integration Hook (CRITICAL)
# ============================================================

def process_revision_directives(context, revision, directives):
    """
    Hook to modify auto-generated migrations for GeoAlchemy2 compatibility.
    
    This function is called by Alembic after generating a migration but
    before writing it to disk. It performs two critical tasks:
    
    1. Auto-import GeoAlchemy2 types
       - Detects use of Geography/Geometry columns
       - Adds necessary imports to migration file
    
    2. Remove duplicate spatial indexes
       - Alembic sometimes generates GIST indexes twice (nested and top-level)
       - This hook detects and removes duplicates to prevent migration errors
    
    Without this hook:
    - Migrations would fail with "ImportError: Geography not found"
    - Migrations would fail with "index already exists" errors
    
    Args:
        context: Alembic migration context
        revision: Revision identifiers (not used)
        directives: List of migration directives to modify
    """
    from alembic.operations import ops
    
    if not directives:
        return
    
    script = directives[0]
    
    if script.upgrade_ops is None:
        return
    
    uses_geoalchemy = False
    
    # --------------------------------------------------------
    # Step 1: Detect GeoAlchemy2 usage and add imports
    # --------------------------------------------------------
    for i, op in enumerate(script.upgrade_ops.ops):
        # Check CreateTableOp for spatial column types
        if isinstance(op, ops.CreateTableOp):
            for column in op.columns:
                col_type = getattr(column, 'type', None)
                if col_type is None:
                    continue
                
                type_str = str(type(col_type))
                
                if 'Geography' in type_str or 'Geometry' in type_str:
                    uses_geoalchemy = True
                    col_name = getattr(column, 'key', getattr(column, 'name', 'unknown'))
                    table_name = getattr(op, 'table_name', 'unknown_table')
                    print(f"[ALEMBIC] Detected spatial type in column '{col_name}' of table '{table_name}'")
        
        # --------------------------------------------------------
        # Step 2: Remove duplicate spatial indexes (nested)
        # --------------------------------------------------------
        if isinstance(op, ops.ModifyTableOps):
            sub_ops = getattr(op, 'ops', [])
            if not sub_ops:
                continue
            
            indices_to_remove = []
            
            for j, sub_op in enumerate(sub_ops):
                if isinstance(sub_op, ops.CreateIndexOp):
                    index_name = getattr(sub_op, 'index_name', 'unknown_index')
                    kw = getattr(sub_op, 'kw', {})
                    columns = getattr(sub_op, 'columns', None)
                    
                    # Detect GIST spatial indexes
                    if kw.get('postgresql_using') == 'gist':
                        if columns:
                            column_names = [str(col) for col in columns]
                            if any('geometry' in col_name.lower() for col_name in column_names):
                                indices_to_remove.append(j)
                                print(f"[ALEMBIC] Removing duplicate spatial index '{index_name}'")
            
            # Remove marked indexes
            for j in reversed(indices_to_remove):
                removed_name = getattr(sub_ops[j], 'index_name', 'unknown_index')
                sub_ops.pop(j)
                print(f"[ALEMBIC] Removed duplicate index: {removed_name}")
    
    # --------------------------------------------------------
    # Step 3: Add GeoAlchemy2 imports if needed
    # --------------------------------------------------------
    if uses_geoalchemy:
        print("[ALEMBIC] Adding GeoAlchemy2 imports to migration")
        
        if script.imports is None:
            script.imports = set()
        
        script.imports.add("import geoalchemy2")
        script.imports.add("from geoalchemy2 import Geography, Geometry")


# ============================================================
# Offline Migration Mode (SQL Script Generation)
# ============================================================

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    Generates SQL migration scripts without connecting to the database.
    Useful for:
    - CI/CD pipelines
    - Manual review before applying changes
    - Deployment to environments without direct database access
    
    Output: SQL file that can be executed with psql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,
        render_as_batch=False,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# Online Migration Mode (Direct Execution)
# ============================================================

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    
    Connects directly to the database and executes migration operations.
    This is the default mode used by:
    - alembic upgrade head
    - alembic downgrade -1
    
    Connection Pool:
    - Uses NullPool to avoid persistent connections
    - Safe for one-time migration execution
    """
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
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# Entry Point: Select Migration Mode
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()