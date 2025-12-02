"""
src/DB/base.py
==========================
SQLAlchemy Model Registry
==========================

This module serves as the central registry for all SQLAlchemy models in the
GPS tracking application. It imports all model classes to ensure they are
registered with SQLAlchemy's metadata system before database operations begin.

Purpose:
--------
By importing all models in a single location, this module ensures that:
1. All tables are discoverable by Alembic for migration generation
2. SQLAlchemy's metadata contains complete schema information
3. Foreign key relationships are properly resolved
4. Database initialization can access all table definitions

Architecture Note:
-----------------
This pattern is essential for:
- **Alembic Migrations**: Without importing models, Alembic cannot detect tables
- **Database Initialization**: create_all() requires models to be imported
- **Relationship Resolution**: SQLAlchemy needs all models loaded for foreign keys

Usage:
------
This module is typically imported in:
- alembic/env.py: To make models available for migration generation
- Database initialization scripts: To create all tables
- Application startup: To ensure metadata is complete

Models Registered:
-----------------
- GPS_data: GPS tracking data from devices (location, speed, heading, etc.)
- Device: Tracking device information (IMEI, model, status, etc.)
- Geofence: Geographic boundary definitions for alerts and monitoring
- AccelerometerData: Accelerometer sensor data for motion analysis
- Trip: Journey records with start/end points and statistics

Important:
----------
Any new model classes MUST be imported here to be included in:
- Automatic migration generation
- Database schema operations
- ORM relationship resolution
"""

from src.DB.base_class import Base

# ============================================================
# MODEL IMPORTS - DO NOT REMOVE
# ============================================================
# Import all models to register them with SQLAlchemy metadata
# These imports are required for Alembic migrations and database operations

from src.Models.gps_data import GPS_data
from src.Models.device import Device  
from src.Models.geofence import Geofence  
from src.Models.accelerometer_data import AccelerometerData
from src.Models.trip import Trip