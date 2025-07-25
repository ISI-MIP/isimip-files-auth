from flask import Flask, abort, request

import jwt
from dotenv import load_dotenv

from .utils import decode_token

load_dotenv()


app = Flask(__name__)


@app.route("/validate", methods=["GET"])
def validate():
    auth_header = request.headers.get("Authorization")
    cookie_token = request.cookies.get("access_token")
    token = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    elif cookie_token:
        token = cookie_token
    else:
        abort(401, "No token provided")

    try:
        payload = decode_token(token)

        token_path = payload.get("path")
        if not token_path:
            abort(403, "No path claim in token")

        requested_path = request.headers.get("X-Original-URI", "/")
        if not requested_path.startswith(token_path):
            abort(403, "Path not authorized")

        return "", 200

    except jwt.ExpiredSignatureError:
        abort(401, "Token expired")
    except jwt.InvalidTokenError:
        abort(401, "Invalid token")
