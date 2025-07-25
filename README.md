ISIMIP Files Auth
=================

A lightweight JWT validation service for the ISIMIP Repository.


Setup
-----

Clone the repo, e.g. to `/srv/www/auth`:

```bash
git clone https://github.com/ISI-MIP/isimip-files-auth /srv/www/auth
```

In **development**, create a `.env` file which contains the secret needed for encoding/decoding the JWT:

```
ISIMIP_FILES_AUTH_SECRET=super-secret
```

The app can be run using `make`.

In **production** create a Systemd service file:

```
# in /etc/systemd/system/auth.service

[Unit]
Description=isimip-files-auth gunicorn daemon
After=network.target

[Service]
User=isimip-files-auth
Group=isimip

WorkingDirectory=/srv/www/auth

Environment=FLASK_APP=isimip_files_auth.app
Environment=FLASK_ENV=production
Environment=ISIMIP_FILES_AUTH_SECRET=super-secret

Environment=GUNICORN_BIN=env/bin/gunicorn
Environment=GUNICORN_WORKER=1
Environment=GUNICORN_PORT=9000
Environment=GUNICORN_TIMEOUT=3
Environment=GUNICORN_PID_FILE=/run/gunicorn/auth/pid
Environment=GUNICORN_ACCESS_LOG_FILE=/var/log/gunicorn/auth/access.log
Environment=GUNICORN_ERROR_LOG_FILE=/var/log/gunicorn/auth/error.log

ExecStart=/bin/sh -c '${GUNICORN_BIN} \
  --workers ${GUNICORN_WORKER} \
  --pid ${GUNICORN_PID_FILE} \
  --bind localhost:${GUNICORN_PORT} \
  --timeout ${GUNICORN_TIMEOUT} \
  --access-logfile ${GUNICORN_ACCESS_LOG_FILE} \
  --error-logfile ${GUNICORN_ERROR_LOG_FILE} \
  "isimip_files_api.app:create_app()"'

ExecReload=/bin/sh -c '/usr/bin/pkill -HUP -F ${GUNICORN_PID_FILE}'

ExecStop=/bin/sh -c '/usr/bin/pkill -TERM -F ${GUNICORN_PID_FILE}'

[Install]
WantedBy=multi-user.target
```

Reload the systemd service files:

```
systemctl daemon-reload
```

Also, create a file `/etc/tmpfiles.d/auth.conf` with the following content:

```
d /var/log/gunicorn/auth  750 isimip-files-auth isimip
d /var/log/flask/auth     750 isimip-files-auth isimip
d /run/gunicorn/auth      750 isimip-files-auth isimip
```

Create temporary directories using:

```
systemd-tmpfiles --create
```

The start the service using:

```
systemctl enable --now auth
```

The service is used as

```
server {
    listen 80;

    location / {
        auth_request /auth;

        ...
    }

    location = /auth {
        internal;
        proxy_pass http://127.0.0.1:9000/validate;
        proxy_pass_request_body off;
        proxy_set_header Authorization $http_authorization;
        proxy_set_header Cookie $http_cookie;
        proxy_set_header X-Original-URI $request_uri;
        proxy_set_header Content-Length "";
    }
}
```
