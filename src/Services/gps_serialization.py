# src/Services/gps_serialization.py

from datetime import datetime, timezone
from typing import Any
from src.Schemas.gps_data import GpsData_get
from src.Models.gps_data import GPS_data


def serialize_gps_row(row: GPS_data | None, include_id: bool = False) -> dict[str, Any] | None:
    """
    Convierte una fila GPS_data de SQLAlchemy en un dict JSON-serializable.

    - Usa el schema Pydantic para validación.
    - include_id: si es True, incluye el campo interno 'id'.
    - Normaliza el timestamp a UTC ISO-8601 con sufijo 'Z'.
    """
    if row is None:
        return None

    exclude_fields = set() if include_id else {"id"}
    # ORM -> dict vía Pydantic
    data = GpsData_get.model_validate(row).model_dump(exclude=exclude_fields)

    # Normalizar timestamp (UTC ISO 8601 con 'Z')
    ts = data.get("Timestamp")
    if isinstance(ts, datetime):
        data["Timestamp"] = ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        data["Timestamp"] = None

    return data


def serialize_many(rows: list[GPS_data], include_id: bool = False) -> list[dict[str, Any]]:
    """
    Convierte una lista de filas GPS_data en una lista de dicts JSON-serializables.

    - Usa `serialize_gps_row` en cada elemento.
    - Filtra automáticamente filas nulas o inválidas.
    - include_id: si es True, incluye el campo interno 'id' en cada dict.
    """
    return [serialized for row in rows if (serialized := serialize_gps_row(row, include_id=include_id)) is not None]

