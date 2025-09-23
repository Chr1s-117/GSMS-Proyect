#!/bin/bash
set -e

# Sanitiza INSTANCE_IDS (quita chars inválidos)
INSTANCE_IDS_CLEAN="$(echo "$INSTANCE_IDS" | sed 's/[^a-zA-Z0-9-,]//g')"
if [ -z "$INSTANCE_IDS_CLEAN" ]; then
  echo "Error: INSTANCE_IDS no definido."
  exit 2
fi

echo "Enviando comando SSM para verificar/crear deploy_from_s3.sh en instancias: $INSTANCE_IDS_CLEAN"

cat <<EOP > fix.json
{
  "DocumentName": "AWS-RunShellScript",
  "Targets": [
    {
      "Key": "InstanceIds",
      "Values": ["$(echo $INSTANCE_IDS_CLEAN | sed 's/,/","/g')"]
    }
  ],
  "Parameters": {
    "commands": [
      "if [ ! -f /usr/local/bin/deploy_from_s3.sh ]; then",
      "  echo \"[FIX] Creando /usr/local/bin/deploy_from_s3.sh...\";",
      "  cat <<\"EOF\" >/usr/local/bin/deploy_from_s3.sh",
      "#!/usr/bin/env bash",
      "set -euo pipefail",
      "",
      "# ====== Configuración (consistente con User Data) ======",
      "REGION=\"${AWS_DEFAULT_REGION:-us-east-1}\"",
      "APP_ROOT=\"/opt/gsms\"",
      "APP_DIR=\"${APP_ROOT}/app\"",
      "VENV_DIR=\"${APP_ROOT}/venv\"",
      "SERVICE_WEB=\"gsms-web.service\"",
      "SERVICE_UDP=\"gsms-udp.service\"",
      "USER_SVC=\"gsms\"",
      "",
      "S3_PATH=\"${1:?Uso: deploy_from_s3.sh s3://bucket/prefix/release_id}\"",
      "",
      "# ====== Pre-chequeos ======",
      "command -v aws >/dev/null || { echo \"Falta AWS CLI\"; exit 20; }",
      "install -d -o \"${USER_SVC}\" -g \"${USER_SVC}\" -m 0755 \"${APP_DIR}/src\"",
      "",
      "# Chequeo adicional: Verifica si venv está inicializado",
      "if [ ! -f \"${VENV_DIR}/bin/pip\" ]; then",
      "  echo \"[ERROR] Venv no inicializado correctamente. Saliendo.\"",
      "  exit 1",
      "fi",
      "",
      "# ====== Sincronización de Código ======",
      "echo \"[Deploy] Sincronizando código desde ${S3_PATH}\"",
      "aws s3 sync \"${S3_PATH%/}/src/\" \"${APP_DIR}/src/\" --delete --exclude \".git/*\" || true",
      "aws s3 sync \"${S3_PATH%/}/\" \"${APP_DIR}/\" --delete --exclude \"src/*\" --exclude \"releases/*\" --exclude \".git/*\" || true",
      "",
      "chown -R ${USER_SVC}:${USER_SVC} \"${APP_DIR}\"",
      "find \"${APP_DIR}\" -type d -name \"__pycache__\" -exec rm -rf {} + || true",
      "",
      "# ====== Instalación Inteligente de Dependencias ======",
      "REQ_FILE=\"\"",
      "[ -f \"${APP_DIR}/requirements.txt\" ] && REQ_FILE=\"${APP_DIR}/requirements.txt\"",
      "[ -z \"$REQ_FILE\" ] && [ -f \"${APP_DIR}/src/requirements.txt\" ] && REQ_FILE=\"${APP_DIR}/src/requirements.txt\"",
      "",
      "if [ -n \"$REQ_FILE\" ]; then",
      "  CURR_SHA=\"$(sha256sum \"$REQ_FILE\" | awk '{print $1}')\"",
      "  PREV_SHA_FILE=\"${APP_ROOT}/.requirements.sha256\"",
      "  PREV_SHA=\"$(cat \"$PREV_SHA_FILE\" 2>/dev/null || echo \"\")\"",
      "  if [ \"$CURR_SHA\" != \"$PREV_SHA\" ]; then",
      "    echo \"[Deps] Cambios en requirements -> instalando...\"",
      "    \"${VENV_DIR}/bin/pip\" install --upgrade pip wheel",
      "    \"${VENV_DIR}/bin/pip\" install -r \"$REQ_FILE\"",
      "    echo \"$CURR_SHA\" > \"$PREV_SHA_FILE\"",
      "  else",
      "    echo \"[Deps] Requirements sin cambios.\"",
      "  fi",
      "else",
      "  echo \"[Deps] No se encontró requirements.txt. Instalando dependencias base...\"",
      "    \"${VENV_DIR}/bin/pip\" install --upgrade pip wheel",
      "    \"${VENV_DIR}/bin/pip\" install fastapi==0.116.1 uvicorn[standard]==0.35.0 SQLAlchemy==2.0.43 alembic==1.16.5 psycopg2-binary==2.9.10 aiosqlite==0.20.0 pydantic==2.11.7 pydantic-settings==2.1.0 requests==2.31.0 Jinja2==3.1.3",
      "fi",
      "",
      "# Chequeo post-instalación",
      "if [ ! -f \"${VENV_DIR}/bin/uvicorn\" ] || ! \"${VENV_DIR}/bin/pip\" list | grep -q pydantic-settings; then",
      "  echo \"[ERROR] Dependencias fallaron.\"",
      "  exit 1",
      "fi",
      "",
      "# ====== Reinicio de Servicios ======",
      "echo \"[Deploy] Reiniciando servicios...\"",
      "systemctl daemon-reload",
      "if systemctl list-unit-files | grep -q \"^${SERVICE_WEB}\"; then",
      "  systemctl restart \"${SERVICE_WEB}\"",
      "  sleep 2",
      "  systemctl --no-pager --full status \"${SERVICE_WEB}\" | tail -n 50 || true",
      "fi",
      "if systemctl list-unit-files | grep -q \"^${SERVICE_UDP}\"; then",
      "  systemctl restart \"${SERVICE_UDP}\" || true",
      "  systemctl --no-pager --full status \"${SERVICE_UDP}\" | tail -n 30 || true",
      "fi",
      "",
      "# ====== Verificación ======",
      "echo \"release=$(basename \"${S3_PATH}\")\" > ${APP_ROOT}/build.txt",
      "curl -sS --max-time 3 http://127.0.0.1:8000/health || echo \"[WARN] /health no respondió.\"",
      "echo \"[Deploy] OK\"",
      "EOF",
      "  chmod +x /usr/local/bin/deploy_from_s3.sh",
      "  sed -i 's/\\r$//' /usr/local/bin/deploy_from_s3.sh",
      "  echo \"Script recreado.\";",
      "else",
      "  echo \"Script ya existe.\";",
      "fi"
    ]
  }
}
EOP

FIX_CMD_ID=$(aws ssm send-command --cli-input-json file://fix.json --query "Command.CommandId" --output text || { echo "Error en send-command fix"; exit 1; })

# Espera fix completado
for j in {1..120}; do
  FIX_STATUS=$(aws ssm list-command-invocations --command-id "$FIX_CMD_ID" --details --query 'CommandInvocations[?Status!=`Success`]' --output json)
  if [ "$FIX_STATUS" = "[]" ]; then
    echo "Fix completado."
    break
  fi
  echo "Fix en progreso... esperando 5s"
  sleep 5
done

if [ "$FIX_STATUS" != "[]" ]; then
  echo "Error: Fix timed out."
  exit 1
fi

# Reintenta deploy original y devuelve nuevo CMD_ID
NEW_CMD_ID=$(aws ssm send-command \
  --document-name "AWS-RunShellScript" \
  --comment "Deploy retry $SHA" \
  --parameters '{"commands":["sudo bash -lc \"/usr/local/bin/deploy_from_s3.sh '"${RELEASE_URI}"'\""]}' \
  --targets "Key=InstanceIds,Values=$INSTANCE_IDS_CLEAN" \
  --query 'Command.CommandId' --output text)

echo "Nuevo CommandId para retry: $NEW_CMD_ID"
echo $NEW_CMD_ID  # Output para capturar en workflow