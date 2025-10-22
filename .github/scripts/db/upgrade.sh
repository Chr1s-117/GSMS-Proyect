#!/usr/bin/env bash
# [AWS-MIGRATION-P3] Ejecuta alembic upgrade head dentro de la instancia EC2

set -euo pipefail

APP_ROOT="/opt/gsms"
APP_DIR="${APP_ROOT}/app"
VENV_DIR="${APP_ROOT}/venv"

# Cargar variables de entorno (DATABASE_URL viene de SSM)
if [ -f /etc/gsms/env ]; then
  set -a
  source /etc/gsms/env
  set +a
fi

# Activar entorno virtual de Python
source "${VENV_DIR}/bin/activate"

cd "${APP_DIR}"

echo "[DB] Running alembic upgrade head..."
alembic upgrade head
echo "[DB] Migration completed successfully."