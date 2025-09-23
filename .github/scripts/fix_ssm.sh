#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C

# Espera variables de entorno:
#   INSTANCE_IDS="i-aaa,i-bbb"
#   RELEASE_URI="s3://bucket/prefix/releases/<SHA>"
: "${INSTANCE_IDS:?INSTANCE_IDS no definido}"
: "${RELEASE_URI:?RELEASE_URI no definido}"

# Sanitizar (solo alfanum, coma o guion)
INSTANCE_IDS_CLEAN="$(printf '%s' "${INSTANCE_IDS}" | tr -cd '[:alnum:],-')"
if [ -z "${INSTANCE_IDS_CLEAN}" ]; then
  echo "Error: INSTANCE_IDS quedó vacío tras sanitizar." >&2
  exit 2
fi

echo "FIX: instancias destino => ${INSTANCE_IDS_CLEAN}"
IFS=',' read -ra IDS <<< "${INSTANCE_IDS_CLEAN}"

# 1) Construir commands.json con el script de reparación + redeploy
#    OJO: usamos 'EOF' para que no se expandan variables del heredoc en el runner
cat > commands.json <<'EOC'
{
  "commands": [
    "set -euxo pipefail",
    "if [ ! -x /usr/local/bin/deploy_from_s3.sh ]; then",
    "  echo \"[FIX] Creando /usr/local/bin/deploy_from_s3.sh...\";",
    "  cat <<'EOF' >/usr/local/bin/deploy_from_s3.sh",
    "#!/usr/bin/env bash",
    "set -euo pipefail",
    "USER_SVC=\"gsms\"",
    "APP_ROOT=\"/opt/gsms\"",
    "APP_DIR=\"${APP_ROOT}/app\"",
    "VENV_DIR=\"${APP_ROOT}/venv\"",
    "S3_PATH=\"${1:?Uso: deploy_from_s3.sh s3://bucket/prefix/release_id}\"",
    "",
    "command -v aws >/dev/null || { echo \"Falta AWS CLI\"; exit 20; }",
    "",
    "# Validar que la ruta S3 tenga contenido",
    "if ! aws s3 ls \"${S3_PATH%/}/\" | grep -q . ; then",
    "  echo \"[ERROR] Ruta S3 inválida o sin objetos: ${S3_PATH}\"",
    "  exit 21",
    "fi",
    "",
    "install -d -o \"${USER_SVC}\" -g \"${USER_SVC}\" -m 0755 \"${APP_DIR}/src\"",
    "",
    "echo \"[deploy] sync ${S3_PATH} -> ${APP_DIR}\"",
    "aws s3 sync \"${S3_PATH%/}/\" \"${APP_DIR}/\" --delete --no-progress",
    "",
    "# (Opcional) instalar deps si existe venv y requirements",
    "REQ_FILE=\"\"",
    "[ -f \"${APP_DIR}/requirements.txt\" ] && REQ_FILE=\"${APP_DIR}/requirements.txt\"",
    "[ -z \"$REQ_FILE\" ] && [ -f \"${APP_DIR}/src/requirements.txt\" ] && REQ_FILE=\"${APP_DIR}/src/requirements.txt\"",
    "if [ -n \"$REQ_FILE\" ] && [ -x \"${VENV_DIR}/bin/pip\" ]; then",
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
    "  echo \"[Deps] Venv no inicializado o sin requirements; omitiendo instalación.\"",
    "fi",
    "",
    "chown -R ${USER_SVC}:${USER_SVC} \"${APP_DIR}\" || true",
    "find \"${APP_DIR}\" -type d -name \"__pycache__\" -exec rm -rf {} + || true",
    "",
    "if command -v systemctl >/dev/null; then",
    "  systemctl daemon-reload || true",
    "  systemctl restart gsms-web  || true",
    "  systemctl restart gsms-udp  || true",
    "fi",
    "echo \"[deploy] OK\"",
    "EOF",
    "  chmod +x /usr/local/bin/deploy_from_s3.sh",
    "  sed -i 's/\\r$//' /usr/local/bin/deploy_from_s3.sh",
    "else",
    "  echo \"[FIX] Script ya existe y es ejecutable.\"",
    "fi"
  ]
}
EOC

# 2) Ejecutar FIX (sin cli-input-json; solo parameters desde archivo)
FIX_CMD_ID=$(aws ssm send-command \
  --instance-ids "${IDS[@]}" \
  --document-name "AWS-RunShellScript" \
  --comment "GSMS FIX: repair deploy_from_s3.sh" \
  --parameters file://commands.json \
  --query "Command.CommandId" --output text)

echo "FIX CommandId: ${FIX_CMD_ID}"

# 3) Esperar hasta 10 min a que todas terminen Success
for j in {1..120}; do
  PENDING=$(aws ssm list-command-invocations \
    --command-id "$FIX_CMD_ID" \
    --details \
    --query "length(CommandInvocations[?Status!='Success'])" \
    --output text || echo "1")
  if [ "$PENDING" = "0" ]; then
    echo "Fix completado en todas las instancias."
    break
  fi
  echo "Fix en progreso... esperando 5s"
  sleep 5
done

# 4) Reintentar deploy con la release exacta
NEW_CMD_ID=$(aws ssm send-command \
  --instance-ids "${IDS[@]}" \
  --document-name "AWS-RunShellScript" \
  --comment "GSMS Deploy retry ${GITHUB_SHA:-unknown}" \
  --parameters "{\"commands\":[\"sudo bash -lc '/usr/local/bin/deploy_from_s3.sh \\\"${RELEASE_URI}\\\"'\"]}" \
  --query 'Command.CommandId' --output text)

echo "Nuevo CommandId para retry: ${NEW_CMD_ID}"
# Output limpio para el workflow:
printf '%s\n' "${NEW_CMD_ID}"