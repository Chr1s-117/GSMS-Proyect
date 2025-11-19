# src/Core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Project metadata
    """
    PROJECT_NAME: str = "GSMS"
    PROJECT_VERSION: str = "5.0.0"
    
    """
    Database URL is required and loaded from environment variables.
    """
    DATABASE_URL: str
    
    """
    Service configuration flags
    """
    UDP_ENABLED: bool = True
    UDP_PORT: int = 9001
    
    # ============================================================
    # 🆕 TRIP DETECTION CONFIGURATION (High Priority)
    # ============================================================
    TRIP_JUMP_THRESHOLD_M: int = 500
    """
    Umbral de salto espacial imposible (metros).
    
    Define la distancia máxima entre dos GPS consecutivos que se considera 
    válida. Si la distancia es mayor, se asume error GPS o reinicio del device.
    
    Valores sugeridos:
    - 2000m (default): Tolerante, permite errores GPS ocasionales
    - 1000m: Más estricto, detecta anomalías más rápido
    - 5000m: Muy tolerante, para zonas con GPS inestable
    
    Impacto:
    - Más bajo: Más trips creados (más sensible a errores GPS)
    - Más alto: Menos trips creados (tolera más ruido GPS)
    """
    
    TRIP_STILL_THRESHOLD_M: int = 700
    """
    Umbral de movimiento mínimo (metros).
    
    Define qué tan lejos debe moverse el vehículo para considerarse "en movimiento".
    Valores menores compensan el ruido natural del GPS (~10-30m).
    
    Valores sugeridos:
    - 50m (default): Balance entre sensibilidad y ruido GPS
    - 30m: Más sensible, detecta movimientos pequeños
    - 100m: Menos sensible, solo movimientos significativos
    
    Impacto:
    - Más bajo: Más sensible (puede crear trips por deriva GPS)
    - Más alto: Menos sensible (ignora movimientos pequeños)
    """
    
    TRIP_PARKING_TIME_S: int = 1200
    """
    Tiempo de inactividad para detectar parking (segundos).
    
    Define cuánto tiempo debe estar quieto el vehículo antes de crear 
    una sesión de parking. Default: 1200s = 20 minutos.
    
    Valores sugeridos:
    - 600s (10 min): Detecta parkings cortos (paradas rápidas)
    - 1200s (20 min): Default, parkings normales
    - 1800s (30 min): Solo parkings prolongados
    
    Impacto:
    - Más bajo: Más sesiones de parking (más granular)
    - Más alto: Menos sesiones de parking (solo las largas)
    """
    
    TRIP_GPS_INTERVAL_S: int = 5
    """
    Intervalo esperado entre puntos GPS (segundos).
    
    Define cada cuántos segundos se espera recibir un GPS del device.
    Usado para calcular STILL_GPS_REQUIRED (cuántos GPS quietos = parking).
    
    Valores sugeridos:
    - 5s (default): Frecuencia estándar de muestreo GPS
    - 10s: Muestreo menos frecuente (ahorra batería/datos)
    - 1s: Muestreo muy frecuente (tracking preciso)
    
    Impacto:
    - Afecta el cálculo de STILL_GPS_REQUIRED
    - NO cambia el comportamiento del hardware (solo expectativa)
    """
    
    # ============================================================
    # 🆕 CACHE CONFIGURATION (Medium Priority)
    # ============================================================
    CACHE_MAX_SIZE: int = 1000
    """
    Tamaño máximo del caché en memoria (número de entries).
    
    Define cuántas respuestas HTTP pueden almacenarse en memoria antes 
    de empezar a evictuar las más antiguas (LRU - Least Recently Used).
    
    Valores sugeridos:
    - 1000 (default): ~1MB RAM, suficiente para 100 usuarios
    - 5000: ~5MB RAM, para más usuarios concurrentes
    - 500: ~500KB RAM, para limitar uso de memoria
    
    Impacto:
    - Más alto: Más memoria usada, menos DB queries
    - Más bajo: Menos memoria usada, más DB queries
    """
    
    CACHE_DEFAULT_TTL_S: int = 300
    """
    Tiempo de vida del caché (segundos).
    
    Define cuánto tiempo una entrada puede permanecer en caché antes 
    de considerarse "stale" y ser removida. Default: 300s = 5 minutos.
    
    Valores sugeridos:
    - 60s (1 min): Datos muy frescos, más DB queries
    - 300s (5 min): Balance entre freshness y performance
    - 600s (10 min): Menos DB queries, datos menos frescos
    
    Impacto:
    - Más alto: Menos DB queries, datos pueden estar desactualizados
    - Más bajo: Más DB queries, datos siempre frescos
    """
    
    class Config:
        env_file = None
        case_sensitive = False

settings = Settings()  # type: ignore