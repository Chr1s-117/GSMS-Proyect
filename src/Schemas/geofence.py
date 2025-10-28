# src/Schemas/geofence.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class GeofenceBase(BaseModel):
    """Schema base para geocercas."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    type: str = Field(default='custom', max_length=50)
    is_active: bool = True
    color: str = Field(default='#3388ff', pattern=r'^#[0-9A-Fa-f]{6}$')
    extra_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        alias='metadata',
        serialization_alias='metadata'
    )


class GeofenceCreate(GeofenceBase):
    """Schema para crear geocerca."""
    id: str = Field(..., min_length=1, max_length=100)
    geometry: Dict[str, Any]  # GeoJSON Polygon


class GeofenceUpdate(BaseModel):
    """Schema para actualizar geocerca (todos los campos opcionales)."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    type: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    geometry: Optional[Dict[str, Any]] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        alias='metadata',
        serialization_alias='metadata'
    )

class GeofenceGet(GeofenceBase):
    """Schema para respuesta de geocerca."""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    # geometry se serializa aparte en el repository