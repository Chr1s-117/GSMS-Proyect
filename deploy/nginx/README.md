# NGINX en GSMS

- Este repo trae `deploy/nginx/gsms.conf` para que NGINX escuche en `:8000` y proxiee a Uvicorn `127.0.0.1:8001`.
- El ALB ya apunta al puerto 8000 del EC2, así que no se cambia nada en AWS.

En el Punto 0.1 (AWS), el user-data:
1) Instalará nginx con `dnf install -y nginx`.
2) Copiará `deploy/nginx/gsms.conf` a `/etc/nginx/conf.d/gsms.conf`.
3) Habilitará y levantará nginx (`systemctl enable --now nginx`).
