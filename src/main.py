# src/main.py

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os

from src.Core.config import settings
from src.Controller.Routes import gps_datas
from src.Services.udp import start_udp_server
from src.Services.ddns import start_ddns_service
from src.Services.gps_broadcaster import start_gps_broadcaster
from src.Services.response_broadcaster import start_response_broadcaster
from src.Core import log_ws, gps_ws, request_ws, response_ws 

# ------------------------------------------------------------
# Utility function to parse comma-separated origins
# ------------------------------------------------------------
def _parse_origins(csv_value: str) -> tuple[bool, list[str]]:
    """
    Parse a comma-separated string of origins.
    If the value is "*", it allows all origins.

    Args:
        csv_value (str): Comma-separated origins or "*".

    Returns:
        allow_all (bool): True if "*" is specified.
        origins_list (list[str]): Clean list of allowed origins.
    """
    if csv_value.strip() == "*":
        return True, ["*"]
    return False, [o.strip() for o in csv_value.split(",") if o.strip()]

# ------------------------------------------------------------
# Load allowed origins from environment variables
# Default to "*" (allow all) if not set
# ------------------------------------------------------------
HTTP_ALLOWED_ORIGINS = os.getenv("HTTP_ALLOWED_ORIGINS", "*")
WS_ALLOWED_ORIGINS = os.getenv("WS_ALLOWED_ORIGINS", "*")

_ws_allow_all, _ws_origins = _parse_origins(WS_ALLOWED_ORIGINS)
_http_allow_all, _http_origins = _parse_origins(HTTP_ALLOWED_ORIGINS)

# ------------------------------------------------------------
# Application lifespan context
# Initializes background services and attaches event loops
# ------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    - Sets up the main asyncio loop for WebSocket managers.
    - Starts UDP server, DDNS service, and GPS broadcaster
      if enabled in settings.
    - Ensures clean shutdown of services.
    """
    loop = asyncio.get_running_loop()

    # Attach main loop to WebSocket managers
    log_ws.log_ws_manager.set_main_loop(loop)
    gps_ws.gps_ws_manager.set_main_loop(loop)
    response_ws.response_ws_manager.set_main_loop(loop)

    # Start Dynamic DNS service if enabled
    if settings.DDNS_ENABLED:
        print("[SERVICES] Starting DDNS updater...")
        start_ddns_service()
    else:
        print("[SERVICES] DDNS service disabled.")

    # Start UDP service if enabled
    if settings.UDP_ENABLED:
        print("[SERVICES] Starting UDP server...")
        start_udp_server()
    else:
        print("[SERVICES] UDP service disabled.")

    # Start GPS broadcaster
    if settings.BROADCASTER_ENABLE:
        print("[SERVICES] Starting GPS broadcaster...")
        start_gps_broadcaster()
    else:
        print("[SERVICES] GPS broadcaster service disabled.")

    print("[SERVICES] Starting response broadcaster...")
    start_response_broadcaster()

    yield
    print("[SERVICES] Shutting down services...")

# ------------------------------------------------------------
# Initialize FastAPI application
# ------------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# ------------------------------------------------------------
# Add CORS middleware for HTTP requests
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=_http_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Health check endpoint
# ------------------------------------------------------------
@app.get("/health")
def health():
    """
    Simple health check endpoint.
    Returns a JSON indicating the server is running.
    """
    return {"status": "ok"}

# ------------------------------------------------------------
# Register REST routes
# ------------------------------------------------------------
app.include_router(gps_datas.router, prefix="/gps_data", tags=["gps_data"])

# ------------------------------------------------------------
# Generic WebSocket handler
# ------------------------------------------------------------
async def socket_handler(ws: WebSocket, manager):
    """
    Generic WebSocket connection handler.

    - Validates the client origin.
    - Registers the WebSocket in the manager.
    - Keeps reading messages until client disconnects.
    - Delegates incoming messages to the manager's handle_message().
    """
    origin = ws.headers.get("origin")
    if (not _ws_allow_all) and (origin not in _ws_origins):
        await ws.close(code=403)
        return

    await manager.register(ws)
    try:
        while True:
            message = await ws.receive_text()
            await manager.handle_message(ws, message)
    except Exception as e:
        print(f"[WS ERROR] {e}")
    finally:
        manager.unregister(ws)

# ------------------------------------------------------------
# WebSocket endpoints
# ------------------------------------------------------------
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
# ------------------------------------------------------------
# Serve Angular frontend and static assets
# ------------------------------------------------------------
frontend_path = os.path.join(os.path.dirname(__file__), "../front/browser")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
