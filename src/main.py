"""
FastAPI Application for GPS Tracking System
============================================
Architecture:
- REST API: All GPS queries via HTTP endpoints with ETag caching
- WebSocket: Live system logs via /logs endpoint
- UDP Server: Receives GPS data from tracking devices
- Background Services: UDP processing and cache management

Version: 2.0.0 (REST-first architecture)
"""
from dotenv import load_dotenv
import os

# ============================================================
# ⚡ CARGAR VARIABLES DE ENTORNO
# ============================================================
load_dotenv()

# ============================================================
# Ahora sí, importar el resto
# ============================================================
from fastapi import FastAPI, WebSocket
from src.Core.config import settings
from src.Controller.Routes import gps_datas
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import asyncio

# Background services
from src.Services.udp import start_udp_server

# WebSocket managers (only logs now)
from src.Core import log_ws

# Database
from src.DB.session import SessionLocal

# Geofence utilities
from src.Repositories.geofence import count_geofences
from src.Services.geofence_importer import geofence_importer

# ============================================================
# ✨ HTTP Cache Middleware (ETag-based caching)
# ============================================================
from src.Middleware.cache_middleware import HTTPCacheMiddleware

# ============================================================
# 🧩 AWS CHANGE #1: ROOT_PATH (subdirectory deployment)
# ============================================================
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse

ROOT_PATH = os.getenv("ROOT_PATH", "").strip()
if ROOT_PATH:
    if not ROOT_PATH.startswith("/"):
        ROOT_PATH = "/" + ROOT_PATH
    if ROOT_PATH.endswith("/"):
        ROOT_PATH = ROOT_PATH[:-1]

class StripPrefixMiddleware(BaseHTTPMiddleware):
    """
    Middleware para eliminar el prefijo ROOT_PATH de las rutas.
    
    Ejemplo:
    - ROOT_PATH="/dev/chris"
    - Request: /dev/chris/gps_data/last
    - FastAPI ve: /gps_data/last
    """
    def __init__(self, app, prefix: str):
        super().__init__(app)
        self.prefix = prefix
    
    async def dispatch(self, request, call_next):
        if self.prefix:
            p = request.url.path
            # Redirect /dev/chris → /dev/chris/
            if p == self.prefix:
                return RedirectResponse(url=self.prefix + "/", status_code=307)
            # Quitar prefijo
            if p.startswith(self.prefix + "/"):
                request.scope["path"] = p[len(self.prefix):] or "/"
        return await call_next(request)

# ============================================================
# 🧩 AWS CHANGE #2: CORS Dinámico (HTTP + WebSocket)
# ============================================================
from fastapi.middleware.cors import CORSMiddleware

def _parse_origins(csv_value: str):
    """
    Convierte CSV de orígenes en lista.
    
    Ejemplos:
    - "*" → wildcard (permitir todos)
    - "https://app.com,https://admin.app.com" → lista de 2 orígenes
    - "" → lista vacía
    """
    if not csv_value:
        return (False, [])
    csv_value = csv_value.strip()
    if csv_value == "*":
        return (True, ["*"])
    origins = [o.strip() for o in csv_value.split(",") if o.strip()]
    return (False, origins)

# Parsear orígenes permitidos desde variables de entorno
_http_allow_all, _http_origins = _parse_origins(
    os.getenv("HTTP_ALLOWED_ORIGINS", "*")
)
_ws_allow_all, _ws_origins = _parse_origins(
    os.getenv("WS_ALLOWED_ORIGINS", "*")
)

# ============================================================
# 🆕 INSTANCE ID MIDDLEWARE (PRESENTACIÓN)
# ============================================================
class InstanceHeaderMiddleware(BaseHTTPMiddleware):
    """
    Agrega X-Instance-ID a todas las respuestas HTTP.
    Solo activo si INSTANCE_ID está en el entorno (AWS).
    
    Para presentaciones: permite identificar a qué instancia EC2
    se conectó el usuario a través del balanceador de carga.
    """
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        instance_id = os.getenv("INSTANCE_ID")
        if instance_id:
            response.headers["X-Instance-ID"] = instance_id
        
        return response

# ============================================================
# APPLICATION LIFESPAN
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Startup:
    - Attach event loop to WebSocket managers
    - Import geofences (if database is empty)
    - Start UDP server (receives GPS from devices)
    
    Shutdown:
    - Background threads terminate automatically (daemon mode)
    """
    
    # ========================================
    # STEP 1: Setup event loop for WebSocket
    # ========================================
    loop = asyncio.get_running_loop()
    log_ws.log_ws_manager.set_main_loop(loop)
    
    # ========================================
    # STEP 2: Import geofences (if needed)
    # ========================================
    geofence_file = Path("data/curated/barranquilla_v1.geojson")
    
    if not geofence_file.exists():
        print("[STARTUP] ⚠️  No geofence file found at data/curated/barranquilla_v1.geojson")
        print("[STARTUP] ⚠️  Skipping geofence import")
    else:
        with SessionLocal() as db:
            count = count_geofences(db, only_active=False)
            
            if count > 0:
                print(f"[STARTUP] ✅ Database already has {count} geofences, skipping import")
            else:
                print("[STARTUP] 📄 Database empty, importing geofences...")
                
                try:
                    created, updated, skipped, failed = geofence_importer.import_from_file(
                        db=db,
                        filepath=str(geofence_file),
                        mode='skip'
                    )
                    
                    print(f"[STARTUP] ✅ Import complete:")
                    print(f"[STARTUP]    Created: {created}")
                    print(f"[STARTUP]    Updated: {updated}")
                    print(f"[STARTUP]    Skipped: {skipped}")
                    print(f"[STARTUP]    Failed: {failed}")
                    
                except Exception as e:
                    print(f"[STARTUP] ❌ Import failed: {e}")
                    import traceback
                    traceback.print_exc()
    
    # ========================================
    # STEP 3: Start UDP server
    # ========================================
    if settings.UDP_ENABLED:
        print("[SERVICES] Starting UDP server...")
        start_udp_server()
    else:
        print("[SERVICES] ⚠️  UDP service disabled")
    
    print("[STARTUP] ✅ Application ready")
    
    yield
    
    # Shutdown
    print("[SHUTDOWN] 🛑 Application stopped")

# ============================================================
# APPLICATION INSTANCE
# ============================================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# ============================================================
# 🧩 REGISTRAR MIDDLEWARES (EL ORDEN IMPORTA)
# ============================================================
# Nota: Los middlewares se ejecutan en ORDEN INVERSO al registro
# (último registrado = primero en ejecutarse)

# 1. StripPrefix (si hay ROOT_PATH)
if ROOT_PATH:
    app.add_middleware(StripPrefixMiddleware, prefix=ROOT_PATH)

# 2. Instance ID Middleware (NUEVO - ANTES de Cache y CORS)
app.add_middleware(InstanceHeaderMiddleware)

# 3. HTTP Cache (tu middleware existente)
app.add_middleware(HTTPCacheMiddleware)

# 4. CORS (debe ir DESPUÉS de Cache para que headers CORS se agreguen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_http_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🧩 AWS CHANGE #3: Health Check Endpoint
# ============================================================
@app.get("/health")
def health():
    """
    Endpoint de health check para AWS.
    
    AWS ALB/ECS usa esto para verificar que el contenedor está vivo.
    Si retorna 200, el contenedor se considera "healthy".
    Si falla varias veces, AWS lo reinicia.
    """
    return {"status": "ok"}

# ============================================================
# REST API ROUTES
# ============================================================
# Register GPS data routes (queries, persistence, analytics)
app.include_router(gps_datas.router, prefix="/gps_data", tags=["gps_data"])

# ============================================================
# WEBSOCKET ENDPOINTS
# ============================================================
async def socket_handler(ws: WebSocket, manager):
    """
    Generic WebSocket connection handler con validación CORS.
    
    - Valida origin contra WS_ALLOWED_ORIGINS
    - Registra WebSocket en el manager
    - Mantiene conexión y procesa mensajes
    """
    origin = ws.headers.get("origin")
    
    # Validar origin (skip si _ws_allow_all == True, o sea "*")
    if (not _ws_allow_all) and (origin not in _ws_origins):
        print(f"[WS] ❌ Rejected from unauthorized origin: {origin}")
        await ws.close(code=403)
        return
    
    await manager.register(ws)
    
    try:
        while True:
            # Receive and process messages from client
            message = await ws.receive_text()
            await manager.handle_message(ws, message)
    except Exception as e:
        # Client disconnected or error occurred
        print(f"[WS] Connection closed: {e}")
    finally:
        manager.unregister(ws)

@app.websocket("/logs")
async def websocket_logs(ws: WebSocket):
    """
    WebSocket endpoint for streaming system logs.
    
    This is the ONLY WebSocket endpoint (GPS data now uses REST).
    
    Frontend connection:
        const ws = new WebSocket('ws://localhost:8000/logs');
    
    Message format:
        {
            "level": "log" | "error" | "warning",
            "message": "...",
            "timestamp": "2025-11-13T10:30:00Z"
        }
    """
    await socket_handler(ws, log_ws.log_ws_manager)

# ============================================================
# FRONTEND STATIC FILES
# ============================================================
# Serve Angular frontend (must be last - catch-all route)
frontend_path = os.path.join(os.path.dirname(__file__), "../front_deploy/browser")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    print(f"[STARTUP] ✅ Frontend mounted at {frontend_path}")
else:
    print(f"[STARTUP] ⚠️  Frontend not found at {frontend_path}")

# ============================================================
# ROOT ENDPOINT (API Info)
# ============================================================
@app.get("/api")
def api_info():
    """
    API information and health check.
    
    Returns system status and available endpoints.
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