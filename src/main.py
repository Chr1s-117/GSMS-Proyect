# src/main.py

"""
GSMS Backend - Main Application Entry Point

Multi-device GPS tracking system with geofence support.

Features:
- FastAPI REST API
- WebSocket real-time communication
- UDP GPS data receiver
- Dynamic DNS updates
- CORS configuration
- Static frontend serving
"""

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
import asyncio
import os

from src.Core.config import settings
from src.Controller.Routes import gps_datas, devices, geofences  # ← AGREGADO devices, geofences
from src.Services.udp import start_udp_server
from src.Services.ddns import start_ddns_service
from src.Services.gps_broadcaster import start_gps_broadcaster
from src.Services.response_broadcaster import start_response_broadcaster
from src.Core import log_ws, gps_ws, request_ws, response_ws  # ← response_ws agregado (debes crear el archivo)

# ============================================
# Configuration
# ============================================

ROOT_PATH = os.getenv("ROOT_PATH", "").strip()
if ROOT_PATH and not ROOT_PATH.startswith("/"):
    ROOT_PATH = "/" + ROOT_PATH
ROOT_PATH = ROOT_PATH.rstrip("/")  # "/dev/chris/" -> "/dev/chris"


# ============================================
# Utility Functions
# ============================================

def _parse_origins(csv_value: str) -> tuple[bool, list[str]]:
    """
    Parse a comma-separated string of origins.
    If the value is "*", it allows all origins.

    Args:
        csv_value: Comma-separated origins or "*".

    Returns:
        allow_all: True if "*" is specified.
        origins_list: Clean list of allowed origins.
    """
    if csv_value.strip() == "*":
        return True, ["*"]
    return False, [o.strip() for o in csv_value.split(",") if o.strip()]


# ============================================
# CORS Configuration
# ============================================

# Load allowed origins from environment variables
# Default to "*" (allow all) if not set
HTTP_ALLOWED_ORIGINS = os.getenv("HTTP_ALLOWED_ORIGINS", "*")
WS_ALLOWED_ORIGINS = os.getenv("WS_ALLOWED_ORIGINS", "*")

_ws_allow_all, _ws_origins = _parse_origins(WS_ALLOWED_ORIGINS)
_http_allow_all, _http_origins = _parse_origins(HTTP_ALLOWED_ORIGINS)


# ============================================
# Application Lifespan
# ============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Startup:
    - Sets up the main asyncio loop for WebSocket managers
    - Starts UDP server, DDNS service, and broadcasters if enabled

    Shutdown:
    - Ensures clean shutdown of services
    """
    loop = asyncio.get_running_loop()

    # Attach main loop to WebSocket managers
    log_ws.log_ws_manager.set_main_loop(loop)
    gps_ws.gps_ws_manager.set_main_loop(loop)
    request_ws.request_ws_manager.set_main_loop(loop)
    response_ws.response_ws_manager.set_main_loop(loop)  # ← AGREGADO

    print("[STARTUP] ============================================")
    print(f"[STARTUP] {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    print(f"[STARTUP] Environment: {settings.APP_ENV}")
    print("[STARTUP] ============================================")

    # Start Dynamic DNS service if enabled
    if settings.DDNS_ENABLED:
        print("[SERVICES] ✅ Starting DDNS updater...")
        start_ddns_service()
    else:
        print("[SERVICES] ⏭️  DDNS service disabled")

    # Start UDP service if enabled
    if settings.UDP_ENABLED:
        print("[SERVICES] ✅ Starting UDP server...")
        start_udp_server()
    else:
        print("[SERVICES] ⏭️  UDP service disabled")

    # Start GPS broadcaster
    if settings.BROADCASTER_ENABLE:
        print("[SERVICES] ✅ Starting GPS broadcaster...")
        start_gps_broadcaster()
    else:
        print("[SERVICES] ⏭️  GPS broadcaster disabled")

    # Start response broadcaster (always enabled)
    print("[SERVICES] ✅ Starting response broadcaster...")
    start_response_broadcaster()

    print("[STARTUP] ============================================")
    print("[STARTUP] All services started successfully")
    print("[STARTUP] ============================================")

    yield

    print("[SHUTDOWN] ============================================")
    print("[SHUTDOWN] Shutting down services...")
    print("[SHUTDOWN] ============================================")


# ============================================
# FastAPI Application
# ============================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)


# ============================================
# Middleware
# ============================================

class StripPrefixMiddleware(BaseHTTPMiddleware):
    """
    Middleware to strip a prefix from request paths.
    
    Useful for deploying behind reverse proxy with path prefix.
    Example: /dev/chris/gps_data → /gps_data
    """
    def __init__(self, app, prefix: str):
        super().__init__(app)
        self.prefix = (prefix or "").rstrip("/")

    async def dispatch(self, request, call_next):
        if self.prefix:
            p = request.url.path
            # Redirect /dev/chris -> /dev/chris/
            if p == self.prefix:
                return RedirectResponse(url=self.prefix + "/", status_code=307)
            # Strip prefix from path
            if p.startswith(self.prefix + "/"):
                request.scope["path"] = p[len(self.prefix):] or "/"
        return await call_next(request)

app.add_middleware(StripPrefixMiddleware, prefix=ROOT_PATH)

# CORS middleware for HTTP requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=_http_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Health Check Endpoint
# ============================================

@app.get("/health")
def health():
    """
    Health check endpoint for AWS ALB/NLB.
    
    Returns:
        {"status": "ok"}
    """
    return {"status": "ok"}


# ============================================
# REST API Routes
# ============================================

app.include_router(
    gps_datas.router, 
    prefix="/gps_data", 
    tags=["GPS Data"]
)

app.include_router(
    devices.router, 
    prefix="/devices", 
    tags=["Devices"]
)  # ← AGREGADO

app.include_router(
    geofences.router, 
    prefix="/geofences", 
    tags=["Geofences"]
)  # ← AGREGADO


# ============================================
# WebSocket Handler
# ============================================

async def socket_handler(ws: WebSocket, manager):
    """
    Generic WebSocket connection handler.

    - Validates the client origin
    - Registers the WebSocket in the manager
    - Keeps reading messages until client disconnects
    - Delegates incoming messages to the manager's handle_message()
    """
    origin = ws.headers.get("origin")
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
        print(f"[WS ERROR] {type(e).__name__}: {e}")
    finally:
        manager.unregister(ws)


# ============================================
# WebSocket Endpoints
# ============================================

@app.websocket("/logs")
async def websocket_logs(ws: WebSocket):
    """WebSocket endpoint for log streaming."""
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


# ============================================
# Static Frontend Serving
# ============================================

frontend_path = os.path.join(os.path.dirname(__file__), "../front/browser")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    print(f"[STARTUP] ✅ Frontend served from: {frontend_path}")
else:
    print(f"[STARTUP] ⚠️  Frontend path not found: {frontend_path}")