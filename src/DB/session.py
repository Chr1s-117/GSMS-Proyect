# src/DB/session.py

"""
Database Session Configuration Module

This module sets up the SQLAlchemy engine and session factory
for connecting to PostgreSQL (local or AWS RDS).

The engine is configured with production-ready settings for:
- Connection pooling and recycling (important for RDS)
- Pre-ping validation to detect stale connections
- Proper timeout handling for network reliability

Environment Compatibility:
- Local: DATABASE_URL from .env file (e.g., postgresql://user:pass@localhost:5432/db)
- AWS: DATABASE_URL from environment variables injected by systemd
      (e.g., postgresql://gsms_user:***@gsms-postgres-prod.*.rds.amazonaws.com:5432/GSMS_DB)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.Core.config import settings


# ============================================================
# SQLAlchemy Engine Configuration
# ============================================================

engine = create_engine(
    settings.DATABASE_URL,
    
    # --- Connection Pool Settings ---
    # These settings are critical for production stability with RDS
    
    pool_pre_ping=True,
    # ✅ Validates connections before using them
    # ✅ Prevents "server closed connection unexpectedly" errors
    # ✅ Essential for RDS which may drop idle connections
    
    pool_recycle=3600,
    # ✅ Recycles connections every 1 hour (3600 seconds)
    # ✅ Prevents using stale connections in long-running services
    # ✅ RDS default timeout is ~8 hours, but recycling earlier is safer
    
    pool_size=5,
    # ✅ Maintains 5 connections in the pool
    # ✅ Suitable for single EC2 instance with moderate load
    # ✅ Adjust based on RDS max_connections (default: 100 for db.t4g.micro)
    
    max_overflow=10,
    # ✅ Allows up to 10 additional connections during traffic spikes
    # ✅ Total max concurrent connections = pool_size + max_overflow = 15
    
    pool_timeout=30,
    # ✅ Wait up to 30 seconds for an available connection
    # ✅ Prevents indefinite hangs if pool is exhausted
    # ✅ Raises TimeoutError if no connection available after 30s
    
    # --- Query Execution Settings ---
    
    echo=False,
    # ✅ Set to True for SQL query logging (useful for debugging)
    # ✅ Keep False in production to avoid log spam
    
    # echo_pool=False,
    # ✅ Uncomment to debug connection pool behavior
    # ✅ Logs connection checkout/checkin events
)


# ============================================================
# Session Factory
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    # ✅ Transactions must be explicitly committed
    # ✅ Prevents accidental auto-commits that could corrupt data
    
    autoflush=False,
    # ✅ Manual control over when changes are flushed to DB
    # ✅ Improves performance by batching operations
    
    bind=engine
    # ✅ Binds this session factory to the engine above
)


# ============================================================
# Connection Validation (Optional Debug Helper)
# ============================================================

def test_connection():
    """
    Test database connectivity.
    
    Useful for debugging connection issues during development
    or verifying configuration in production.
    
    Usage:
        from src.DB.session import test_connection
        test_connection()
    
    Raises:
        Exception: If connection fails
    """
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print(f"[DB] ✅ Connection successful: {result.scalar()}")
    except Exception as e:
        print(f"[DB] ❌ Connection failed: {e}")
        raise


# ============================================================
# Development Notes
# ============================================================

"""
Pool Sizing Recommendations:

1. Single EC2 instance (current setup):
   - pool_size=5, max_overflow=10 (total: 15 connections)

2. Multiple EC2 instances (future scaling):
   - Calculate: (pool_size + max_overflow) * num_instances < RDS max_connections
   - Example: 3 instances × 15 connections = 45 total (safe for RDS default 100)

3. RDS max_connections by instance type:
   - db.t4g.micro:  ~100 connections
   - db.t4g.small:  ~200 connections
   - db.t4g.medium: ~400 connections

RDS Connection Limits:
- Check current limit: SELECT * FROM pg_settings WHERE name = 'max_connections';
- Monitor usage: SELECT count(*) FROM pg_stat_activity;

Troubleshooting:
- "too many connections" error → Reduce pool_size or increase RDS instance size
- "server closed connection" error → Ensure pool_pre_ping=True
- Slow queries → Enable echo=True temporarily to debug SQL
"""