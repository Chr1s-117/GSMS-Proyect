# Systemd en GSMS

- `gsms-web.service` arranca Uvicorn en `127.0.0.1:8001`.
- En el Punto 0.1, el user-data copiará este unit a `/etc/systemd/system/gsms-web.service`,
  creará el drop-in `env.conf` (con variables desde SSM) y hará:
    systemctl daemon-reload
    systemctl enable --now gsms-web.service