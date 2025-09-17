"""
This script sets up the Alembic environment for running database migrations.
It supports both "offline" (SQL script generation) and "online" (direct execution)
migration modes. Environment variables are loaded from a .env file for secure
configuration of database connection URLs.
"""
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
from src.DB.base_class import Base
from src.Models.gps_data import GPS_data


_ = GPS_data.__table__  # Ensure the table definitions are loaded by referencing GPS_data

# -------------------------------------------------------------------
# Load environment variables from .env file
# -------------------------------------------------------------------

"""
Using python-dotenv to securely load DATABASE_URL and other sensitive
configuration from a .env file. This avoids hardcoding credentials.
"""
load_dotenv()

config = context.config # Alembic configuration object

# -------------------------------------------------------------------
# Set the SQLAlchemy database URL dynamically from environment variables
# -------------------------------------------------------------------

"""
This allows the application to adapt to different environments (development,
staging, production) without modifying the Alembic config file.
"""
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment variables")


config.set_main_option("sqlalchemy.url", database_url) # Update Alembic config with the database URL

# -------------------------------------------------------------------
# Configure Python logging using the Alembic config file if available
# -------------------------------------------------------------------

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------------------------
# Set target metadata for Alembic autogeneration
# -------------------------------------------------------------------

"""
Alembic uses this metadata to compare the database schema with models
and generate migration scripts.
"""
target_metadata = Base.metadata

# -------------------------------------------------------------------
# Offline migrations
# -------------------------------------------------------------------

"""
In "offline" mode, SQL statements are generated as a script and not executed
directly against the database. Useful for CI/CD pipelines or review before
applying changes.
"""

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode. Generates SQL migration scripts
    without connecting to the database.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,  # Embed values directly in generated SQL
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------------------------
# Online migrations
# -------------------------------------------------------------------

"""
In "online" mode, Alembic connects directly to the database and executes
migration operations.
"""
def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode. Executes migration scripts directly
    against the connected database.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Avoids persistent DB connections
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------------------------
# Execute appropriate migration mode
# -------------------------------------------------------------------

"""
Alembic automatically detects if it should run in offline or online mode.
"""
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
