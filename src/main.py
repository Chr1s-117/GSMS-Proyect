from fastapi import FastAPI, WebSocket, HTTPException
from src.Core.config import settings
from src.Controller.Routes import gps_datas
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from src.Services.udp import start_udp_server
from src.Services.gps_broadcaster import start_gps_broadcaster
from src.Services.response_broadcaster import start_response_broadcaster
from src.Core import log_ws, gps_ws, request_ws, response_ws   
from src.DB.session import SessionLocal  
from pathlib import Path
from src.Repositories.geofence import count_geofences
from src.Services.geofence_importer import geofence_importer
import asyncio
import os

# ============================================================
# 🧩 FASE 1: ROOT_PATH y StripPrefixMiddleware
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
    """Middleware para eliminar el prefijo ROOT_PATH en las rutas entrantes."""

    def __init__(self, app, prefix: str):
        super().__init__(app)
        self.prefix = prefix

    async def dispatch(self, request, call_next):
        # ✅ Corrección: redirect antes de modificar el path
        if self.prefix:
            p = request.url.path

            # Redirigir /dev/chris → /dev/chris/
            if p == self.prefix:
                return RedirectResponse(url=self.prefix + "/", status_code=307)

            # Quitar prefijo solo si empieza con prefix + "/"
            if p.startswith(self.prefix + "/"):
                request.scope["path"] = p[len(self.prefix):] or "/"

        return await call_next(request)


# ============================================================
# 🧩 FASE 2: Sistema CORS Dinámico
# ============================================================
from fastapi.middleware.cors import CORSMiddleware


def _parse_origins(csv_value: str):
    """Convierte variable CSV de orígenes en lista normalizada o wildcard."""
    if not csv_value:
        return (False, [])
    csv_value = csv_value.strip()
    if csv_value == "*":
        return (True, ["*"])
    origins = [o.strip() for o in csv_value.split(",") if o.strip()]
    return (False, origins)


# ✅ Corrección: permitir "*" por defecto si no hay variables
_http_allow_all, _http_origins = _parse_origins(os.getenv("HTTP_ALLOWED_ORIGINS", "*"))
_ws_allow_all, _ws_origins = _parse_origins(os.getenv("WS_ALLOWED_ORIGINS", "*"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context.
    This function is executed when the FastAPI app starts and stops.
    It initializes background services and registers event loops
    for the WebSocket managers.
    """
    loop = asyncio.get_running_loop()

    # Attach main event loop to WebSocket managers
    log_ws.log_ws_manager.set_main_loop(loop)
    gps_ws.gps_ws_manager.set_main_loop(loop)
    response_ws.response_ws_manager.set_main_loop(loop)

    # ============================================================
    # ✅ NUEVO: Importar geocercas al arrancar
    # ============================================================
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
    # ============================================================

    # Start UDP service if enabled
    if settings.UDP_ENABLED:
        print("[SERVICES] Starting UDP server...")
        start_udp_server()
    else:
        print("[SERVICES] UDP service disabled.")

    # Start GPS broadcaster
    print("[SERVICES] Starting GPS broadcaster...")
    start_gps_broadcaster()

    print("[SERVICES] Starting response broadcaster...")
    start_response_broadcaster()

    yield
    print("Shutting down services...")


# ============================================================
# 🧩 Inicialización de la aplicación FastAPI
# ============================================================
# ✅ Corrección: remover root_path del constructor
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# ============================================================
# 🧩 FASE 1: Conexión del middleware StripPrefix
# ============================================================
if ROOT_PATH:
    app.add_middleware(StripPrefixMiddleware, prefix=ROOT_PATH)

# ============================================================
# 🧩 FASE 3: CORSMiddleware para HTTP
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=_http_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🧩 FASE 4: Health Check Endpoint
# ============================================================
@app.get("/health")
def health():
    return {"status": "ok"}


# Register REST routes (GPS data persistence / queries)
app.include_router(gps_datas.router, prefix="/gps_data", tags=["gps_data"])


# ============================================================
# 🧩 FASE 5: Validación WebSocket Dinámica + FASE 6: Logs de errores
# ============================================================
async def socket_handler(ws: WebSocket, manager):
    """
    Generic WebSocket connection handler.

    - Validates the client origin (CORS).
    - Registers the WebSocket in the provided manager.
    - Keeps reading messages until the client disconnects.
    - Delegates incoming messages to the manager’s handle_message() method.
    """
    origin = ws.headers.get("origin")
    if (not _ws_allow_all) and (origin not in _ws_origins):
        await ws.close(code=403)
        return

    await manager.register(ws)
    try:
        while True:
            # Receive and process messages from the client
            message = await ws.receive_text()
            await manager.handle_message(ws, message)
    except Exception as e:
        # Cliente desconectado o error
        print(f"[WS ERROR] {e}")
    finally:
        manager.unregister(ws)


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


frontend_path = os.path.join(os.path.dirname(__file__), "../front_deploy/browser")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")