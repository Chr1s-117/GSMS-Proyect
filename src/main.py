"""
src/main.py
============================================
FastAPI Application for GPS Tracking System
============================================

This module serves as the main entry point for a production-grade GPS tracking system
built with FastAPI. The application implements a hybrid architecture that combines
REST API endpoints for GPS data queries with UDP reception for real-time device data.

Architecture Overview:
---------------------
- REST API: All GPS queries are handled via HTTP endpoints with ETag-based caching
- WebSocket: Real-time system logs streamed via /logs endpoint
- UDP Server: Receives GPS data packets from tracking devices
- Background Services: Asynchronous UDP processing and cache management

Version: 2.0.0 (REST-first architecture)
Author: [Your Name/Team]
License: [Your License]
"""

# Environment Configuration
from dotenv import load_dotenv
import os
load_dotenv()

# FastAPI Core
from fastapi import FastAPI, WebSocket
from src.Core.config import settings
from src.Controller.Routes import gps_datas
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import asyncio

# Background Services
from src.Services.udp import start_udp_server

# WebSocket Management (system logs only)
from src.Core import log_ws

# Database
from src.DB.session import SessionLocal

# Geofence Management
from src.Repositories.geofence import count_geofences
from src.Services.geofence_importer import geofence_importer

# ============================================================
# HTTP CACHE MIDDLEWARE
# ============================================================
from src.Middleware.cache_middleware import HTTPCacheMiddleware

# ============================================================
# AWS DEPLOYMENT CONFIGURATION #1: ROOT PATH HANDLING
# ============================================================
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse

# Extract root path for subdirectory deployment (e.g., /api/v1)
ROOT_PATH = os.getenv("ROOT_PATH", "").strip()
if ROOT_PATH:
    if not ROOT_PATH.startswith("/"):
        ROOT_PATH = "/" + ROOT_PATH
    if ROOT_PATH.endswith("/"):
        ROOT_PATH = ROOT_PATH[:-1]


class StripPrefixMiddleware(BaseHTTPMiddleware):
    """
    Middleware for removing ROOT_PATH prefix from incoming requests.
    
    This enables deployment in subdirectories without modifying route definitions.
    
    Example:
        ROOT_PATH = "/dev/chris"
        Incoming request: /dev/chris/gps_data/last
        FastAPI receives: /gps_data/last
    
    Args:
        app: The FastAPI application instance
        prefix: The URL prefix to strip from requests
    """
    
    def __init__(self, app, prefix: str):
        super().__init__(app)
        self.prefix = prefix
    
    async def dispatch(self, request, call_next):
        """
        Process incoming request and strip prefix if applicable.
        
        Args:
            request: The incoming HTTP request
            call_next: Next middleware in the chain
            
        Returns:
            Response from the application
        """
        if self.prefix:
            path = request.url.path
            
            # Redirect bare prefix to prefix with trailing slash
            if path == self.prefix:
                return RedirectResponse(url=self.prefix + "/", status_code=307)
            
            # Remove prefix from path
            if path.startswith(self.prefix + "/"):
                request.scope["path"] = path[len(self.prefix):] or "/"
        
        return await call_next(request)


# ============================================================
# AWS DEPLOYMENT CONFIGURATION #2: DYNAMIC CORS CONFIGURATION
# ============================================================
from fastapi.middleware.cors import CORSMiddleware


def _parse_origins(csv_value: str):
    """
    Parse comma-separated origin values into a list for CORS configuration.
    
    This function converts environment variable strings into proper CORS origin lists,
    supporting both wildcard and explicit origin configurations.
    
    Args:
        csv_value: Comma-separated string of allowed origins
        
    Returns:
        Tuple of (is_wildcard: bool, origins: list)
        
    Examples:
        "*" → (True, ["*"])  # Allow all origins
        "https://app.com,https://admin.app.com" → (False, ["https://app.com", "https://admin.app.com"])
        "" → (False, [])  # No origins allowed
    """
    if not csv_value:
        return (False, [])
    
    csv_value = csv_value.strip()
    
    if csv_value == "*":
        return (True, ["*"])
    
    origins = [origin.strip() for origin in csv_value.split(",") if origin.strip()]
    return (False, origins)


# Parse allowed origins from environment variables
_http_allow_all, _http_origins = _parse_origins(
    os.getenv("HTTP_ALLOWED_ORIGINS", "*")
)
_ws_allow_all, _ws_origins = _parse_origins(
    os.getenv("WS_ALLOWED_ORIGINS", "*")
)


# ============================================================
# INSTANCE IDENTIFICATION MIDDLEWARE
# ============================================================
class InstanceHeaderMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds X-Instance-ID header to all HTTP responses.
    
    This middleware is active only when INSTANCE_ID environment variable is set,
    typically in AWS EC2/ECS deployments. It enables tracking which instance
    handled each request in load-balanced environments.
    
    Use case:
        In presentations or debugging, this allows you to identify which EC2 instance
        behind the load balancer processed a given request.
    
    Response headers:
        X-Instance-ID: i-0123456789abcdef0
    """
    
    async def dispatch(self, request, call_next):
        """
        Process request and add instance identifier to response.
        
        Args:
            request: The incoming HTTP request
            call_next: Next middleware in the chain
            
        Returns:
            Response with X-Instance-ID header if INSTANCE_ID is configured
        """
        response = await call_next(request)
        
        instance_id = os.getenv("INSTANCE_ID")
        if instance_id:
            response.headers["X-Instance-ID"] = instance_id
        
        return response


# ============================================================
# APPLICATION LIFESPAN MANAGEMENT
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Handles application startup and shutdown procedures in a clean, async manner.
    This function is called once when the application starts and once when it stops.
    
    Startup Sequence:
        1. Configure event loop for WebSocket managers
        2. Import geofence data if database is empty
        3. Start UDP server for receiving GPS data from devices
    
    Shutdown Sequence:
        - Background threads terminate automatically (daemon mode)
        - Database connections are closed
        - WebSocket connections are gracefully disconnected
    
    Args:
        app: The FastAPI application instance
        
    Yields:
        Control to the application during its runtime
    """
    
    # ========================================
    # STARTUP: Configure WebSocket Event Loop
    # ========================================
    loop = asyncio.get_running_loop()
    log_ws.log_ws_manager.set_main_loop(loop)
    
    # ========================================
    # STARTUP: Import Geofences if Needed
    # ========================================
    geofence_file = Path("data/curated/barranquilla_v1.geojson")
    
    if not geofence_file.exists():
        print("[STARTUP] ⚠️  Geofence file not found at data/curated/barranquilla_v1.geojson")
        print("[STARTUP] ⚠️  Skipping geofence import")
    else:
        with SessionLocal() as db:
            count = count_geofences(db, only_active=False)
            
            if count > 0:
                print(f"[STARTUP] ✅ Database contains {count} geofences, skipping import")
            else:
                print("[STARTUP] 📄 Empty database detected, importing geofences...")
                
                try:
                    created, updated, skipped, failed = geofence_importer.import_from_file(
                        db=db,
                        filepath=str(geofence_file),
                        mode='skip'
                    )
                    
                    print(f"[STARTUP] ✅ Geofence import completed:")
                    print(f"[STARTUP]    • Created: {created}")
                    print(f"[STARTUP]    • Updated: {updated}")
                    print(f"[STARTUP]    • Skipped: {skipped}")
                    print(f"[STARTUP]    • Failed: {failed}")
                    
                except Exception as e:
                    print(f"[STARTUP] ❌ Geofence import failed: {e}")
                    import traceback
                    traceback.print_exc()
    
    # ========================================
    # STARTUP: Initialize UDP Server
    # ========================================
    if settings.UDP_ENABLED:
        print("[SERVICES] Starting UDP server for GPS data reception...")
        start_udp_server()
    else:
        print("[SERVICES] ⚠️  UDP service is disabled")
    
    print("[STARTUP] ✅ Application initialization complete")
    
    # Application runtime
    yield
    
    # ========================================
    # SHUTDOWN: Cleanup
    # ========================================
    print("[SHUTDOWN] 🛑 Application shutdown initiated")


# ============================================================
# APPLICATION INSTANCE CREATION
# ============================================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)


# ============================================================
# MIDDLEWARE REGISTRATION
# ============================================================
# IMPORTANT: Middlewares are executed in REVERSE order of registration
# (last registered = first executed)

# 1. Root Path Handler (if subdirectory deployment is configured)
if ROOT_PATH:
    app.add_middleware(StripPrefixMiddleware, prefix=ROOT_PATH)

# 2. Instance Identification (must be before Cache and CORS)
app.add_middleware(InstanceHeaderMiddleware)

# 3. HTTP Cache Layer (ETag-based caching)
app.add_middleware(HTTPCacheMiddleware)

# 4. CORS Configuration (must be after Cache to ensure CORS headers are added)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_http_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# AWS DEPLOYMENT CONFIGURATION #3: HEALTH CHECK ENDPOINT
# ============================================================
@app.get("/health")
def health():
    """
    Health check endpoint for AWS infrastructure.
    
    This endpoint is used by AWS Application Load Balancer (ALB) and ECS
    to verify that the container is operational and ready to serve traffic.
    
    Behavior:
        - Returns 200 OK when the application is healthy
        - If this endpoint fails repeatedly, AWS will restart the container
    
    Returns:
        dict: Status object indicating application health
    """
    return {"status": "ok"}


# ============================================================
# REST API ROUTE REGISTRATION
# ============================================================
# Register GPS data routes (queries, persistence, analytics)
app.include_router(gps_datas.router, prefix="/gps_data", tags=["gps_data"])


# ============================================================
# WEBSOCKET ENDPOINTS
# ============================================================
async def socket_handler(ws: WebSocket, manager):
    """
    Generic WebSocket connection handler with CORS validation.
    
    This function manages the complete WebSocket lifecycle:
    1. Validates the request origin against allowed WebSocket origins
    2. Registers the WebSocket connection with the appropriate manager
    3. Maintains the connection and processes incoming messages
    4. Handles disconnection and cleanup
    
    Args:
        ws: WebSocket connection instance
        manager: WebSocket manager for this connection type
        
    Security:
        Validates origin header against WS_ALLOWED_ORIGINS environment variable.
        Connections from unauthorized origins are rejected with a 403 status code.
    """
    origin = ws.headers.get("origin")
    
    # Validate origin (skip validation if wildcard is enabled)
    if (not _ws_allow_all) and (origin not in _ws_origins):
        print(f"[WS] ❌ Connection rejected - unauthorized origin: {origin}")
        await ws.close(code=403)
        return
    
    await manager.register(ws)
    
    try:
        # Main message processing loop
        while True:
            message = await ws.receive_text()
            await manager.handle_message(ws, message)
    except Exception as e:
        # Handle disconnection or processing errors
        print(f"[WS] Connection closed: {e}")
    finally:
        # Ensure cleanup occurs regardless of how the connection ended
        manager.unregister(ws)


@app.websocket("/logs")
async def websocket_logs(ws: WebSocket):
    """
    WebSocket endpoint for streaming real-time system logs.
    
    This is the primary WebSocket endpoint in the application. GPS data
    is now served via REST API, making this the sole WebSocket endpoint.
    
    Frontend Connection Example:
        const ws = new WebSocket('ws://localhost:8000/logs');
        ws.onmessage = (event) => {
            const log = JSON.parse(event.data);
            console.log(`[${log.level}] ${log.message}`);
        };
    
    Message Format:
        {
            "level": "log" | "error" | "warning",
            "message": "Log message content",
            "timestamp": "2025-12-01T10:30:00Z"
        }
    
    Args:
        ws: WebSocket connection instance
    """
    await socket_handler(ws, log_ws.log_ws_manager)


# ============================================================
# FRONTEND STATIC FILE SERVING
# ============================================================
# Serve Angular frontend application (must be registered last - catch-all route)
frontend_path = os.path.join(os.path.dirname(__file__), "../front_deploy/browser")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    print(f"[STARTUP] ✅ Frontend application mounted at {frontend_path}")
else:
    print(f"[STARTUP] ⚠️  Frontend application not found at {frontend_path}")


# ============================================================
# API INFORMATION ENDPOINT
# ============================================================
@app.get("/api")
def api_info():
    """
    API information and system status endpoint.
    
    Provides comprehensive information about the API's current state,
    enabled features, and available endpoints. Useful for API discovery
    and system monitoring.
    
    Returns:
        dict: System status and configuration information including:
            - status: Current operational status
            - version: Application version
            - architecture: System architecture description
            - features: Enabled features and their configurations
            - endpoints: Available API endpoints
    """
    return {
        "status": "online",
        "version": settings.PROJECT_VERSION,
        "architecture": "REST + UDP",
        "features": {
            "http_cache": "ETag-based (304 Not Modified)",
            "websockets": ["/logs"],
            "udp_enabled": settings.UDP_ENABLED,
            "instance_tracking": bool(os.getenv("INSTANCE_ID"))
        },
        "endpoints": {
            "gps_data": "/gps_data/*",
            "logs": "/logs (WebSocket)",
            "health": "/health"
        }
    }