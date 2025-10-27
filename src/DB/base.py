# src/DB/base.py

"""
SQLAlchemy Models Registry

This module imports all SQLAlchemy models to ensure they are registered
with the Base metadata before Alembic generates migrations.

CRITICAL: All models must be imported here for Alembic to detect them.

Workflow:
1. Define model in src/Models/<model_name>.py
2. Import model here
3. Run: alembic revision --autogenerate -m "Add <model_name>"
4. Review migration in alembic/versions/
5. Apply: alembic upgrade head

Current Models:
- GPS_data: GPS tracking data from devices
- Device: Registered devices in the system
- Geofence: Geographic boundaries for alerts
"""

from src.DB.base_class import Base

# ============================================================
# Import all models here
# ============================================================
# Each model must be imported to be included in Alembic migrations

from src.Models.gps_data import GPS_data    # ✅ Core tracking model
from src.Models.device import Device        # ✅ Device registry
from src.Models.geofence import Geofence    # ✅ Geofence definitions


# ============================================================
# Model Registry Validation (Optional Development Tool)
# ============================================================

def list_registered_models():
    """
    List all registered SQLAlchemy models.
    
    Useful for debugging Alembic migrations to verify all models
    are properly imported and registered.
    
    Usage:
        from src.DB.base import list_registered_models
        list_registered_models()
    """
    print("[DB] 📋 Registered SQLAlchemy Models:")
    for mapper in Base.registry.mappers:
        print(f"  - {mapper.class_.__name__} → Table: {mapper.class_.__tablename__}")


# ============================================================
# Development Notes
# ============================================================

"""
Adding New Models:

1. Create model file:
   src/Models/my_new_model.py

2. Import here:
   from src.Models.my_new_model import MyNewModel

3. Generate migration:
   alembic revision --autogenerate -m "Add MyNewModel table"

4. Review generated migration in alembic/versions/

5. Apply migration:
   alembic upgrade head

Common Issues:

- "Alembic not detecting new model"
  → Verify model is imported in this file
  → Check model inherits from Base

- "Table already exists" error
  → Migration was partially applied
  → Check alembic_version table in database
  → May need to stamp database: alembic stamp head

- "Multiple heads" error
  → Multiple migration branches exist
  → Merge branches: alembic merge heads
"""