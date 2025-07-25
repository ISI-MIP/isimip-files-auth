# set environment variables for `flask run` for development
# in production, the variables should be set in systemd
export FLASK_APP=isimip_files_auth.app
export FLASK_ENV=development
export FLASK_DEBUG=true

server:
	flask run

gunicorn:
	gunicorn -b 0.0.0.0:9000 "${FLASK_APP}:app"

.PHONY: server
