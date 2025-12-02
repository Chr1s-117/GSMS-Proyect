"""
src/Core/config.py
=================================
Application Configuration Module
=================================

This module defines the centralized configuration system for the GPS tracking
application using Pydantic Settings. All configuration parameters are loaded
from environment variables and validated at startup.

Architecture:
------------
- Pydantic BaseSettings: Type-safe configuration with automatic validation
- Environment Variables: All sensitive data (DATABASE_URL) sourced from .env
- Default Values: Sensible defaults for optional parameters
- Type Safety: Static type checking for all configuration values

Configuration Categories:
------------------------
1. **Project Metadata**: Application name and version
2. **Database**: Connection string (required)
3. **Services**: UDP server configuration
4. **Trip Detection**: Spatial and temporal thresholds for journey detection
5. **Cache**: HTTP response caching parameters

Environment Variables:
---------------------
Required:
    - DATABASE_URL: PostgreSQL connection string with PostGIS extension

Optional (with defaults):
    - UDP_ENABLED: Enable/disable UDP GPS data reception (default: True)
    - UDP_PORT: UDP listener port (default: 9001)
    - TRIP_JUMP_THRESHOLD_M: Maximum valid distance between GPS points
    - TRIP_STILL_THRESHOLD_M: Minimum movement distance to detect motion
    - TRIP_PARKING_TIME_S: Idle time before parking detection
    - TRIP_GPS_INTERVAL_S: Expected GPS sampling interval
    - CACHE_MAX_SIZE: Maximum cached responses in memory
    - CACHE_DEFAULT_TTL_S: Cache entry time-to-live

Usage Example:
-------------
    from src.Core.config import settings
    
    # Access configuration values
    print(f"Connecting to: {settings.DATABASE_URL}")
    print(f"UDP Port: {settings.UDP_PORT}")
    print(f"Trip jump threshold: {settings.TRIP_JUMP_THRESHOLD_M}m")
    
    # Configuration is read-only and validated at startup
    if settings.UDP_ENABLED:
        start_udp_server(port=settings.UDP_PORT)

Note:
    Configuration validation occurs at module import time. Invalid values
    or missing required variables will raise validation errors immediately,
    ensuring fail-fast behavior during application startup.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings with environment variable support.
    
    This class defines all configurable parameters for the GPS tracking system.
    Values are automatically loaded from environment variables or use default
    values when specified.
    
    Configuration is validated at startup using Pydantic's type system, ensuring
    type safety and preventing runtime errors from misconfiguration.
    """
    
    # ============================================================
    # PROJECT METADATA
    # ============================================================
    PROJECT_NAME: str = "GSMS"
    """Application name identifier."""
    
    PROJECT_VERSION: str = "5.0.0"
    """Current application version following semantic versioning."""
    
    # ============================================================
    # DATABASE CONFIGURATION
    # ============================================================
    DATABASE_URL: str
    """
    PostgreSQL database connection string (required).
    
    Format: postgresql://user:password@host:port/database
    
    Requirements:
        - PostgreSQL 12+ with PostGIS extension enabled
        - Connection pooling is handled by SQLAlchemy
    
    Example:
        postgresql://gps_user:secure_pass@localhost:5432/gps_tracking
    """
    
    # ============================================================
    # SERVICE CONFIGURATION
    # ============================================================
    UDP_ENABLED: bool = True
    """
    Enable UDP server for receiving GPS data from tracking devices.
    
    When enabled, the application listens for GPS packets on UDP_PORT.
    Set to False to disable GPS reception (useful for testing or API-only mode).
    """
    
    UDP_PORT: int = 9001
    """
    UDP port for GPS data reception.
    
    Tracking devices send GPS packets to this port. Ensure this port is:
    - Open in firewall rules
    - Not conflicting with other services
    - Accessible from device network (public IP or VPN)
    """
    
    # ============================================================
    # TRIP DETECTION CONFIGURATION
    # ============================================================
    TRIP_JUMP_THRESHOLD_M: int = 700
    """
    Maximum valid distance between consecutive GPS points (meters).
    
    This threshold detects impossible spatial jumps caused by:
    - GPS signal errors or multipath interference
    - Device reboot or power cycle
    - Location spoofing or tampering
    
    When consecutive GPS points exceed this distance, the system assumes
    an anomaly and ends the current trip, starting a new one.
    
    Recommended Values:
        - 500m (default): Balanced sensitivity for urban/highway environments
        - 1000m: More tolerant of GPS errors in areas with poor signal
        - 2000m: Very permissive, suitable for areas with unstable GPS
        - 300m: Strict detection for high-precision applications
    
    Impact:
        - Lower values: More trips created, higher sensitivity to GPS errors
        - Higher values: Fewer trips, more tolerance for signal noise
    
    Performance Consideration:
        This check runs on every GPS point, so keep threshold reasonable.
    """

    TRIP_STILL_THRESHOLD_M: int = 5
    """
    Minimum movement distance to consider vehicle in motion (meters).
    
    This threshold compensates for GPS drift when the vehicle is stationary.
    Consumer GPS has typical accuracy of 5-30m, causing apparent movement
    even when the device is stationary.
    
    The system considers a vehicle "still" if it moves less than this distance
    over the configured time period.
    
    Recommended Values:
        - 700m (default): Standard threshold for vehicle tracking
        - 30m: High sensitivity, detects small movements (may trigger on GPS drift)
        - 100m: Balanced sensitivity for urban environments
        - 50m: Detect short movements (e.g., parking lot repositioning)
    
    Impact:
        - Lower values: More sensitive to small movements (risk of false positives)
        - Higher values: Only significant movements detected (may miss short trips)
    
    Relationship:
        Works with TRIP_PARKING_TIME_S to determine parking sessions.
    """
    
    TRIP_PARKING_TIME_S: int = 1800
    """
    Idle time threshold for parking detection (seconds).
    
    Defines how long a vehicle must remain stationary (within TRIP_STILL_THRESHOLD_M)
    before the system creates a parking session and ends the current trip.
    
    Default: 1200 seconds = 20 minutes
    
    Recommended Values:
        - 600s (10 min): Detect short stops (e.g., quick errands, deliveries)
        - 1200s (20 min): Standard parking detection (typical stops)
        - 1800s (30 min): Only detect extended parking (long-term stops)
        - 300s (5 min): Very sensitive, captures brief stops (may be too granular)
    
    Impact:
        - Lower values: More parking sessions, more granular trip segmentation
        - Higher values: Fewer parking sessions, only significant stops recorded
    
    Use Cases:
        - Fleet management: 600-900s (detect loading/unloading)
        - Personal tracking: 1200-1800s (typical errands and appointments)
        - Long-haul trucking: 1800-3600s (rest stops and overnight parking)
    
    Calculation:
        System uses (TRIP_PARKING_TIME_S / TRIP_GPS_INTERVAL_S) GPS points
        to confirm stationary state before creating parking session.
    """
    
    TRIP_GPS_INTERVAL_S: int = 5
    """
    Expected GPS sampling interval (seconds).
    
    Defines the expected time between consecutive GPS transmissions from
    tracking devices. This value is used for temporal calculations in
    trip detection algorithms.
    
    Recommended Values:
        - 5s (default): Standard tracking frequency (balanced battery/precision)
        - 10s: Lower frequency (better battery life, less precision)
        - 1s: High frequency (real-time tracking, higher data/battery cost)
        - 30s: Low frequency (long battery life, suitable for slow-moving assets)
    
    Impact:
        - Affects STILL_GPS_REQUIRED calculation (parking detection sensitivity)
        - Does NOT control device hardware (only system expectations)
        - Lower values = more GPS points required for parking confirmation
    
    Note:
        This is an EXPECTED value, not a hardware control parameter. Actual
        device sampling rate is configured on the tracking device itself.
        
    Formula:
        STILL_GPS_REQUIRED = TRIP_PARKING_TIME_S / TRIP_GPS_INTERVAL_S
        
        Example: 1200s / 5s = 240 GPS points must be stationary for parking
    """
    MAX_TIME_GAP_SECONDS: int = 900
    # ============================================================
    # HTTP CACHE CONFIGURATION
    # ============================================================
    CACHE_MAX_SIZE: int = 1000
    """
    Maximum number of cached HTTP responses in memory.
    
    The cache uses LRU (Least Recently Used) eviction policy. When the cache
    reaches this size, the oldest unused entries are removed to make space
    for new responses.
    
    Memory Estimation:
        - Average response size: ~1-2 KB
        - 1000 entries ≈ 1-2 MB RAM
        - 5000 entries ≈ 5-10 MB RAM
    
    Recommended Values:
        - 1000 (default): Suitable for 100-500 concurrent users
        - 5000: High-traffic deployments (500+ concurrent users)
        - 500: Memory-constrained environments or low traffic
        - 100: Development/testing environments
    
    Impact:
        - Higher values: More memory usage, fewer database queries
        - Lower values: Less memory usage, more database queries
    
    Performance Consideration:
        Cache hits provide 50-100x faster response than database queries.
        Size appropriately based on available RAM and traffic patterns.
    """
    
    CACHE_DEFAULT_TTL_S: int = 300
    """
    Default cache entry time-to-live (seconds).
    
    Defines how long cached responses remain valid before being considered
    stale and removed. Stale entries are automatically cleaned up by a
    background task.
    
    Default: 300 seconds = 5 minutes
    
    Recommended Values:
        - 60s (1 min): Real-time applications requiring fresh data
        - 300s (5 min): Balanced freshness and performance (default)
        - 600s (10 min): High-performance mode, can tolerate stale data
        - 30s: Ultra-fresh data requirements (financial, real-time tracking)
    
    Impact:
        - Higher values: Fewer database queries, data may be outdated
        - Lower values: More database queries, always fresh data
    
    Use Cases:
        - Real-time tracking dashboard: 30-60s
        - Historical reports/analytics: 600-1800s
        - Device status checks: 60-300s
        - Geofence queries (rarely change): 600-3600s
    
    Note:
        Individual endpoints can override this value using cache decorators.
        ETag-based validation allows clients to efficiently check freshness.
    """
    
    class Config:
        """Pydantic configuration for settings management."""
        
        env_file = None
        """
        Disable automatic .env file loading.
        
        Environment variables are loaded explicitly in main.py using
        python-dotenv, giving more control over the loading process.
        """
        
        case_sensitive = False
        """
        Allow case-insensitive environment variable names.
        
        Both DATABASE_URL and database_url will be accepted.
        """


# ============================================================
# SETTINGS INSTANCE
# ============================================================
settings = Settings()  # type: ignore
"""
Global settings instance.

This singleton is imported throughout the application to access
configuration values. Validation occurs immediately on import.

Type ignore comment: Suppresses Pydantic validation warnings in
static type checkers while maintaining runtime validation.
"""