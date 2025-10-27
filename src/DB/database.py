# src/DB/database.py

"""
Database Dependency Injection Module

This module provides the database session generator used throughout
the FastAPI application via dependency injection pattern.

The get_db() function is the PRIMARY way to obtain database sessions
in the application, ensuring proper lifecycle management (creation,
usage, and cleanup) of SQLAlchemy sessions.

Key Features:
- Automatic session creation and cleanup
- Compatible with FastAPI Depends()
- Exception-safe (cleanup in finally block)
- Supports background tasks and manual usage
- Thread-safe (each request gets its own session)

Environment Compatibility:
- Local: Uses DATABASE_URL from .env
- AWS: Uses DATABASE_URL from systemd environment

Integration:
- Used in FastAPI endpoint dependencies
- Used in background tasks (UDP receiver, broadcasters)
- Used in startup/shutdown hooks
- Used in manual database operations

Usage Examples:
    # 1. FastAPI Endpoint (Primary Usage)
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from src.DB.database import get_db
    
    @router.get("/devices")
    def list_devices(db: Session = Depends(get_db)):
        devices = db.query(Device).all()
        return devices
    
    # 2. Background Task
    from src.DB.database import get_db
    
    def process_gps_data():
        db = next(get_db())
        try:
            # Process data
            gps_records = db.query(GPS_data).filter(...).all()
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
        finally:
            db.close()
    
    # 3. Startup/Shutdown Hook
    from src.DB.database import get_db
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db = next(get_db())
        try:
            # Initialize data
            setup_initial_data(db)
            db.commit()
        finally:
            db.close()
        
        yield  # App runs
        
        # Cleanup
        print("Shutting down...")

Performance Considerations:
- Each HTTP request gets a dedicated session (isolated transactions)
- Sessions are pooled via SQLAlchemy engine (configured in session.py)
- Connection pooling prevents excessive database connections
- pre_ping validation ensures connections are alive before use

Thread Safety:
- SessionLocal() creates thread-local sessions
- Safe for concurrent requests (each gets its own session)
- Background threads must call get_db() separately

Created: 2025-10-27
Author: Chr1s-117
"""

from typing import Generator
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.DB.session import SessionLocal, engine


# ============================================================
# Primary Database Session Generator
# ============================================================

def get_db() -> Generator[Session, None, None]:
    """
    Database session generator for FastAPI dependency injection.
    
    This is the PRIMARY and RECOMMENDED way to obtain database sessions
    throughout the application. It ensures proper session lifecycle:
    1. Creates a new session from SessionLocal()
    2. Yields session to caller (endpoint, service, etc.)
    3. Ensures cleanup (close) even if exceptions occur
    
    The session is NOT automatically committed - caller must explicitly
    call db.commit() for write operations. This prevents accidental
    data corruption and gives full transaction control to the caller.
    
    Yields:
        Session: SQLAlchemy database session with active transaction
        
    Lifecycle:
        1. Request arrives → get_db() called via Depends()
        2. New session created from connection pool
        3. Session yielded to endpoint handler
        4. Handler executes (read/write operations)
        5. Handler returns (success or exception)
        6. finally block executes → db.close()
        7. Connection returned to pool
    
    Example - Read Operation:
        from fastapi import Depends
        from sqlalchemy.orm import Session
        from src.DB.database import get_db
        
        @router.get("/devices")
        def list_devices(db: Session = Depends(get_db)):
            # Session automatically managed
            devices = db.query(Device).all()
            return devices  # No commit needed for reads
    
    Example - Write Operation:
        @router.post("/devices")
        def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
            new_device = Device(**device.dict())
            db.add(new_device)
            db.commit()  # ✅ Explicit commit required
            db.refresh(new_device)
            return new_device
    
    Example - Error Handling:
        @router.post("/devices")
        def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
            try:
                new_device = Device(**device.dict())
                db.add(new_device)
                db.commit()
                return new_device
            except Exception as e:
                db.rollback()  # ✅ Rollback on error
                raise HTTPException(status_code=400, detail=str(e))
    
    Example - Manual Usage (Background Tasks):
        def background_task():
            db = next(get_db())
            try:
                # Process data
                result = db.query(GPS_data).filter(...).all()
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Background task error: {e}")
            finally:
                db.close()  # ✅ Always cleanup
    
    Notes:
        - Session is thread-local (safe for concurrent requests)
        - Connection is borrowed from pool (not a new TCP connection)
        - Transactions auto-rollback if not committed before close
        - Idle connections recycled per session.py pool_recycle setting
        
    Performance:
        - Session creation: ~1ms (from pool)
        - Session cleanup: ~0.5ms (return to pool)
        - No performance penalty vs manual session management
    
    See Also:
        - src/DB/session.py: Connection pool configuration
        - src/Controller/deps.py: Legacy get_DB() wrapper
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# Database Health Check Utilities
# ============================================================

def test_db_connection() -> bool:
    """
    Test database connectivity with a simple query.
    
    Useful for:
    - Application startup validation
    - Health check endpoints
    - Monitoring and alerting
    - Debugging connection issues
    
    Returns:
        bool: True if database is reachable and responsive, False otherwise
        
    Example - Startup Validation:
        from src.DB.database import test_db_connection
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            print("[STARTUP] 🔍 Testing database connection...")
            if not test_db_connection():
                print("[STARTUP] ❌ Database connection failed!")
                raise Exception("Cannot connect to database")
            print("[STARTUP] ✅ Database connection successful")
            
            yield  # App runs
    
    Example - Health Check Endpoint:
        from src.DB.database import test_db_connection
        
        @app.get("/health")
        def health():
            db_healthy = test_db_connection()
            return {
                "status": "ok" if db_healthy else "error",
                "database": "connected" if db_healthy else "disconnected"
            }
    
    Example - Monitoring Script:
        import time
        from src.DB.database import test_db_connection
        
        while True:
            if not test_db_connection():
                print("[MONITOR] ⚠️  Database connection lost!")
                # Send alert
            time.sleep(60)
    
    Performance:
        - Executes simple SELECT 1 query (~1-5ms)
        - Uses connection from pool (no new connection created)
        - Safe to call frequently for monitoring
    
    Notes:
        - Catches all exceptions (connection errors, timeouts, etc.)
        - Does not raise exceptions (returns False on error)
        - Logs error details to console for debugging
    """
    db = None
    try:
        db = next(get_db())
        # Execute simple test query
        result = db.execute(text("SELECT 1"))
        value = result.scalar()
        return value == 1
    except Exception as e:
        print(f"[DB] ❌ Connection test failed: {e}")
        return False
    finally:
        if db:
            db.close()


def get_db_info() -> dict:
    """
    Get database connection and version information.
    
    Returns detailed information about the database connection,
    including PostgreSQL version, PostGIS version (if installed),
    and connection pool status.
    
    Useful for:
    - Debugging connection issues
    - Verifying PostGIS installation
    - Monitoring connection pool usage
    - System information endpoints
    
    Returns:
        dict: Database information with keys:
            - connected (bool): Whether connection succeeded
            - postgres_version (str): PostgreSQL version string
            - postgis_version (str): PostGIS version or "Not installed"
            - database_name (str): Current database name
            - pool_size (int): Connection pool size
            - pool_checked_out (int): Active connections
            - error (str): Error message if connection failed
    
    Example - Admin Info Endpoint:
        from src.DB.database import get_db_info
        
        @app.get("/admin/db-info")
        def database_info():
            return get_db_info()
    
    Example - Startup Logging:
        from src.DB.database import get_db_info
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            info = get_db_info()
            print(f"[STARTUP] 📊 Database Info:")
            print(f"  PostgreSQL: {info.get('postgres_version', 'Unknown')}")
            print(f"  PostGIS: {info.get('postgis_version', 'Not installed')}")
            print(f"  Database: {info.get('database_name', 'Unknown')}")
            print(f"  Pool Size: {info.get('pool_size', 'Unknown')}")
            
            yield  # App runs
    
    Example Response:
        {
            "connected": true,
            "postgres_version": "PostgreSQL 15.4 on aarch64-unknown-linux-gnu",
            "postgis_version": "3.3.3",
            "database_name": "GSMS_DB",
            "pool_size": 5,
            "pool_checked_out": 2
        }
    
    Performance:
        - Executes 2-3 simple queries (~5-10ms total)
        - Uses connection from pool
        - Safe for admin endpoints (not for high-frequency calls)
    
    Notes:
        - Returns partial info if some queries fail
        - PostGIS version query fails gracefully if extension not installed
        - Pool stats reflect current moment (changes over time)
    """
    db = None
    info = {
        "connected": False,
        "postgres_version": "Unknown",
        "postgis_version": "Not installed",
        "database_name": "Unknown",
        "pool_size": engine.pool.size(),
        "pool_checked_out": engine.pool.checkedout()
    }
    
    try:
        db = next(get_db())
        info["connected"] = True
        
        # Get PostgreSQL version
        result = db.execute(text("SELECT version()"))
        info["postgres_version"] = result.scalar()
        
        # Get current database name
        result = db.execute(text("SELECT current_database()"))
        info["database_name"] = result.scalar()
        
        # Try to get PostGIS version (may fail if not installed)
        try:
            result = db.execute(text("SELECT PostGIS_version()"))
            info["postgis_version"] = result.scalar()
        except Exception:
            info["postgis_version"] = "Not installed"
        
        return info
        
    except Exception as e:
        info["error"] = str(e)
        print(f"[DB] ❌ Failed to get database info: {e}")
        return info
        
    finally:
        if db:
            db.close()


# ============================================================
# Connection Pool Monitoring
# ============================================================

def get_pool_status() -> dict:
    """
    Get current connection pool status and statistics.
    
    Provides real-time information about SQLAlchemy connection pool
    usage, including active connections, available connections, and
    overflow status.
    
    Useful for:
    - Performance monitoring
    - Identifying connection leaks
    - Capacity planning
    - Debugging "too many connections" errors
    
    Returns:
        dict: Pool status with keys:
            - size (int): Maximum pool size (base connections)
            - checked_out (int): Currently active connections
            - overflow (int): Connections beyond pool_size
            - checked_in (int): Available connections in pool
            - max_overflow (int): Maximum overflow allowed
            - timeout (int): Pool timeout in seconds
    
    Example - Monitoring Endpoint:
        from src.DB.database import get_pool_status
        
        @app.get("/admin/pool-status")
        def pool_status():
            return get_pool_status()
    
    Example - Performance Logging:
        import time
        from src.DB.database import get_pool_status
        
        @app.middleware("http")
        async def log_pool_usage(request, call_next):
            start = time.time()
            response = await call_next(request)
            duration = time.time() - start
            
            if duration > 1.0:  # Slow request
                pool = get_pool_status()
                print(f"[SLOW] {request.url.path}: {duration:.2f}s")
                print(f"[POOL] Active: {pool['checked_out']}/{pool['size']}")
            
            return response
    
    Example Response:
        {
            "size": 5,
            "checked_out": 2,
            "overflow": 0,
            "checked_in": 3,
            "max_overflow": 10,
            "timeout": 30
        }
    
    Interpretation:
        - checked_out = 0: No active queries (idle)
        - checked_out = size: Pool fully utilized (normal under load)
        - overflow > 0: Temporary burst (check if sustained)
        - checked_out + overflow = size + max_overflow: Pool exhausted!
    
    Troubleshooting:
        - High checked_out: Many concurrent queries (may need more pool_size)
        - Non-zero overflow: Temporary spikes (normal for burst traffic)
        - Sustained overflow: Increase pool_size in session.py
        - Pool exhausted: Connection leak or need higher limits
    
    Performance:
        - Instant (reads pool object attributes)
        - No database queries executed
        - Safe to call frequently
    
    See Also:
        - src/DB/session.py: Pool configuration (pool_size, max_overflow)
    """
    return {
        "size": engine.pool.size(),
        "checked_out": engine.pool.checkedout(),
        "overflow": engine.pool.overflow(),
        "checked_in": engine.pool.size() - engine.pool.checkedout(),
        "max_overflow": engine.pool._max_overflow,
        "timeout": engine.pool._timeout
    }


# ============================================================
# Development and Testing Utilities
# ============================================================

def create_all_tables():
    """
    Create all database tables defined in models.
    
    WARNING: Only use in development/testing environments.
    In production, use Alembic migrations instead.
    
    This function creates tables by importing Base.metadata from
    src/DB/base.py (which imports all models) and calling create_all().
    
    Use Cases:
        - Local development setup
        - Integration test setup
        - Temporary/throwaway databases
    
    NOT Recommended For:
        - Production databases (use Alembic migrations)
        - Databases with existing data (may fail on conflicts)
        - Schema evolution (no migration history)
    
    Example - Development Setup:
        from src.DB.database import create_all_tables
        
        if __name__ == "__main__":
            print("Creating tables...")
            create_all_tables()
            print("Tables created successfully!")
    
    Example - Test Setup:
        import pytest
        from src.DB.database import create_all_tables, drop_all_tables
        
        @pytest.fixture(scope="session")
        def setup_database():
            create_all_tables()  # Setup
            yield
            drop_all_tables()    # Teardown
    
    Notes:
        - Idempotent: Safe to call multiple times (skips existing tables)
        - Does NOT drop existing tables
        - Does NOT migrate existing schemas
        - Requires database CREATE TABLE permissions
    
    See Also:
        - Alembic: alembic upgrade head (RECOMMENDED for production)
        - drop_all_tables(): Cleanup utility
    """
    from src.DB.base import Base
    print("[DB] 🔨 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("[DB] ✅ Tables created successfully")


def drop_all_tables():
    """
    Drop all database tables defined in models.
    
    WARNING: DESTRUCTIVE OPERATION - USE WITH EXTREME CAUTION.
    This permanently deletes all tables and data.
    
    Only use in development/testing environments.
    NEVER use in production.
    
    Use Cases:
        - Clean test environment after tests
        - Reset development database
        - Teardown temporary databases
    
    NOT Recommended For:
        - Production databases (NEVER!)
        - Databases with important data
        - Shared development databases
    
    Example - Test Teardown:
        import pytest
        from src.DB.database import create_all_tables, drop_all_tables
        
        @pytest.fixture(scope="session")
        def setup_database():
            create_all_tables()
            yield
            drop_all_tables()  # Cleanup after tests
    
    Example - Reset Development Database:
        from src.DB.database import drop_all_tables, create_all_tables
        
        if __name__ == "__main__":
            response = input("⚠️  Drop all tables? (yes/no): ")
            if response.lower() == "yes":
                drop_all_tables()
                create_all_tables()
                print("✅ Database reset complete")
    
    Notes:
        - Irreversible: All data is permanently lost
        - Drops tables in correct order (respects foreign keys)
        - Requires database DROP TABLE permissions
        - Does NOT drop Alembic version table
    
    See Also:
        - create_all_tables(): Create tables after dropping
        - Alembic: alembic downgrade base (RECOMMENDED for production)
    """
    from src.DB.base import Base
    print("[DB] 🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("[DB] ✅ Tables dropped successfully")


# ============================================================
# Module Metadata
# ============================================================

__all__ = [
    "get_db",
    "test_db_connection",
    "get_db_info",
    "get_pool_status",
    "create_all_tables",
    "drop_all_tables"
]