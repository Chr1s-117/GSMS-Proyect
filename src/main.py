# src/main.py

"""
GSMS FastAPI Application - Main Entry Point

This module initializes the FastAPI application and configures:
- Background services (UDP, GPS broadcaster, response broadcaster, DDNS)
- WebSocket endpoints for real-time communication
- CORS middleware for HTTP and WebSocket security
- Static file serving for the Angular frontend
- Database initialization and geofence import on startup

Environment-Specific Behavior:
- Production (dassify.tech): UDP enabled, DDNS enabled, ROOT_PATH=""
- Dev/Chris (dassify.tech/dev/chris): UDP disabled, ROOT_PATH="/dev/chris"
- Dev/Laura (dassify.tech/dev/laura): UDP disabled, ROOT_PATH="/dev/laura"
- Dev/Jose (dassify.tech/dev/jose): UDP disabled, ROOT_PATH="/dev/jose"

Configuration is loaded from environment variables via src.Core.config.settings
"""
from src.Controller.Routes import gps_datas, devices, geofences
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
import asyncio
import os

# Core configuration
from src.Core.config import settings

# Routes
from src.Controller.Routes import gps_datas

# Services
from src.Services.udp import start_udp_server
from src.Services.gps_broadcaster import start_gps_broadcaster
from src.Services.response_broadcaster import start_response_broadcaster

# WebSocket managers
from src.Core import log_ws, gps_ws, request_ws, response_ws

# Database and repositories (for geofence import)
from src.DB.session import SessionLocal
from src.Repositories.geofence import count_geofences
from src.Services.geofence_importer import GeofenceImporter
from src.DB.database import get_db

# DDNS service removed - no longer needed in current infrastructure
# The server now uses static IP assigned by AWS EIP (Elastic IP)
# If dynamic DNS is needed in the future, consider:
#   - AWS Route 53 with dynamic updates
#   - CloudWatch Events + Lambda for IP monitoring


# ------------------------------------------------------------
# ROOT_PATH Configuration
# Used for reverse proxy scenarios (e.g., ALB path-based routing)
# Examples: "", "/dev/chris", "/dev/laura", "/dev/jose"
# ------------------------------------------------------------
#ROOT_PATH = os.getenv("ROOT_PATH", "").strip()
#if ROOT_PATH and not ROOT_PATH.startswith("/"):
#    ROOT_PATH = "/" + ROOT_PATH
#ROOT_PATH = ROOT_PATH.rstrip("/")  # Normalize: "/dev/chris/" -> "/dev/chris"
#
#print(f"[STARTUP] 🔧 ROOT_PATH configured as: '{ROOT_PATH or '(root)'}'")


# ------------------------------------------------------------
# Utility function to parse comma-separated origins
# ------------------------------------------------------------
def _parse_origins(csv_value: str) -> tuple[bool, list[str]]:
    """
    Parse a comma-separated string of origins for CORS validation.
    
    Args:
        csv_value (str): Comma-separated origins or "*" for allow-all.
    
    Returns:
        tuple[bool, list[str]]: (allow_all_flag, origins_list)
        
    Examples:
        "*" -> (True, ["*"])
        "https://example.com,https://app.com" -> (False, ["https://example.com", "https://app.com"])
    """
    if csv_value.strip() == "*":
        return True, ["*"]
    return False, [o.strip() for o in csv_value.split(",") if o.strip()]


# ------------------------------------------------------------
# Load allowed origins from environment variables
# Defaults to "*" (allow all) if not set
# ------------------------------------------------------------
HTTP_ALLOWED_ORIGINS = os.getenv("HTTP_ALLOWED_ORIGINS", "*")
WS_ALLOWED_ORIGINS = os.getenv("WS_ALLOWED_ORIGINS", "*")

_ws_allow_all, _ws_origins = _parse_origins(WS_ALLOWED_ORIGINS)
_http_allow_all, _http_origins = _parse_origins(HTTP_ALLOWED_ORIGINS)

print(f"[STARTUP] 🌐 HTTP CORS: {_http_origins}")
print(f"[STARTUP] 🔌 WebSocket CORS: {_ws_origins}")


# ------------------------------------------------------------
# Application lifespan context
# Initializes background services and database setup
# ------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Startup:
    - Attaches asyncio event loop to WebSocket managers
    - Imports geofences from GeoJSON if database is empty
    - Starts background services (UDP, DDNS, GPS broadcaster, etc.)
    
    Shutdown:
    - Gracefully stops background tasks
    """
    loop = asyncio.get_running_loop()

    # Attach main event loop to WebSocket managers
    print("[STARTUP] 🔗 Attaching event loop to WebSocket managers...")
    log_ws.log_ws_manager.set_main_loop(loop)
    gps_ws.gps_ws_manager.set_main_loop(loop)
    response_ws.response_ws_manager.set_main_loop(loop)

    # ============================================================
    # Database Initialization: Import Geofences on First Run
    # ============================================================
    geofence_file = Path("data/curated/barranquilla_v1.geojson")
    if geofence_file.exists():
        try:
            # Inicializar con una sesión de DB
            db_session = next(get_db())
            importer = GeofenceImporter(db_session)
            
            created, updated, skipped, failed = importer.import_from_file(
                str(geofence_file)
            )
            
            print(f"[GEOFENCE-STARTUP] ✅ Imported: {created} created, {updated} updated, {failed} failed")
            
            db_session.close()
        except Exception as e:
            print(f"[GEOFENCE-STARTUP] ⚠️  Could not import geofences: {e}")
    else:
        print("[STARTUP] 🗄️  Checking geofence database...")
        try:
            with SessionLocal() as db:
                count = count_geofences(db, only_active=False)
                
                if count > 0:
                    print(f"[STARTUP] ✅ Database already has {count} geofences, skipping import")
                else:
                    print("[STARTUP] 📄 Database empty, importing geofences...")
                    
                    # Use the GeofenceImporter class (already imported) with the active DB session
                    importer = GeofenceImporter(db)
                    created, updated, skipped, failed = importer.import_from_file(
                        str(geofence_file)
                    )
                    
                    print(f"[STARTUP] ✅ Geofence import complete:")
                    print(f"[STARTUP]    ➕ Created: {created}")
                    print(f"[STARTUP]    🔄 Updated: {updated}")
                    print(f"[STARTUP]    ⏭️  Skipped: {skipped}")
                    print(f"[STARTUP]    ❌ Failed: {failed}")
                    
        except Exception as e:
            print(f"[STARTUP] ❌ Geofence import failed: {e}")
            import traceback
            traceback.print_exc()

    # ============================================================
    # Start Background Services (Conditional Based on Config)
    # ============================================================
    
    # UDP server (disabled in dev environments via DISABLE_UDP=1)
    if settings.UDP_ENABLED:
        print("[SERVICES] 📡 Starting UDP server...")
        start_udp_server()
    else:
        print("[SERVICES] ⏸️  UDP service disabled (DISABLE_UDP=1)")

    # GPS broadcaster (broadcasts GPS data to connected WebSocket clients)
    if settings.BROADCASTER_ENABLE:
        print("[SERVICES] 📍 Starting GPS broadcaster...")
        start_gps_broadcaster()
    else:
        print("[SERVICES] ⏸️  GPS broadcaster disabled")

    # Response broadcaster (always enabled)
    print("[SERVICES] 💬 Starting response broadcaster...")
    start_response_broadcaster()

    print("[SERVICES] ✅ All services started successfully")

    yield
    
    print("[SHUTDOWN] 🛑 Shutting down services...")


# ------------------------------------------------------------
# Initialize FastAPI application
# ------------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)


# ------------------------------------------------------------
# CORS Middleware (HTTP requests)
# Configured via HTTP_ALLOWED_ORIGINS environment variable
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=_http_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("[STARTUP] 🔐 CORS middleware configured for HTTP")


# ------------------------------------------------------------
# Health check endpoint (required by AWS ALB/NLB)
# ------------------------------------------------------------
@app.get("/health")
def health():
    """
    Health check endpoint for load balancer monitoring.
    
    Returns:
        dict: {"status": "ok"}
    """
    return {"status": "ok"}


# ------------------------------------------------------------
# Register REST API routes
# ------------------------------------------------------------
app.include_router(gps_datas.router, prefix="/gps_data", tags=["gps_data"])
app.include_router(devices.router, prefix="/devices", tags=["devices"]) 
app.include_router(geofences.router, prefix="/geofences", tags=["geofences"])  

# ------------------------------------------------------------
# Generic WebSocket handler with CORS validation
# ------------------------------------------------------------
async def socket_handler(ws: WebSocket, manager):
    """
    Generic WebSocket connection handler with origin validation.
    
    - Validates the client origin against WS_ALLOWED_ORIGINS
    - Registers the WebSocket in the provided manager
    - Keeps reading messages until the client disconnects
    - Delegates incoming messages to the manager's handle_message()
    
    Args:
        ws (WebSocket): The WebSocket connection
        manager: WebSocket manager (log_ws, gps_ws, etc.)
    """
    origin = ws.headers.get("origin")
    
    # CORS validation for WebSocket
    if (not _ws_allow_all) and (origin not in _ws_origins):
        print(f"[WS] ❌ Rejected connection from unauthorized origin: {origin}")
        await ws.close(code=403)
        return

    await manager.register(ws)
    try:
        while True:
            message = await ws.receive_text()
            await manager.handle_message(ws, message)
    except Exception as e:
        print(f"[WS] ⚠️  Connection error: {e}")
    finally:
        manager.unregister(ws)


# ------------------------------------------------------------
# WebSocket endpoints
# ------------------------------------------------------------
@app.websocket("/logs")
async def websocket_logs(ws: WebSocket):
    """WebSocket endpoint for log and error streaming."""
    await socket_handler(ws, log_ws.log_ws_manager)

@app.websocket("/gps")
async def websocket_gps(ws: WebSocket):
    """WebSocket endpoint for GPS data broadcasting."""
    await socket_handler(ws, gps_ws.gps_ws_manager)

@app.websocket("/request")
async def websocket_request(ws: WebSocket):
    """WebSocket endpoint for request handling."""
    await socket_handler(ws, request_ws.request_ws_manager)

@app.websocket("/response")
async def websocket_response(ws: WebSocket):
    """WebSocket endpoint for response handling."""
    await socket_handler(ws, response_ws.response_ws_manager)


# ------------------------------------------------------------
# Serve Angular frontend and static assets
# ------------------------------------------------------------
frontend_path = os.path.join(os.path.dirname(__file__), "../front_deploy/browser")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    print(f"[STARTUP] 🎨 Serving frontend from {frontend_path}")
else:
    print(f"[STARTUP] ⚠️  Frontend path not found: {frontend_path}")
    print("[STARTUP] ⚠️  Static files will not be served")


# ------------------------------------------------------------
# Direct execution support (for local development)
# Not used in production (Uvicorn is started via systemd)
# ------------------------------------------------------------
"""
For local development, run:
    python -m src.main

Or use uvicorn directly:
    uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

In production (AWS), systemd starts Uvicorn with:
    /opt/gsms/venv/bin/uvicorn src.main:app \
        --host 0.0.0.0 --port ${PORT} \
        --root-path ${ROOT_PATH} \
        --proxy-headers --forwarded-allow-ips=*

Environment variables (PORT, ROOT_PATH, etc.) are injected by systemd
from /etc/gsms/env and /etc/gsms/dev/<name>.env
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=settings.PORT,
        reload=True
    )