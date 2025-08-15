from flask import Flask, abort, request

from dotenv import load_dotenv

from .utils import validate_token

load_dotenv()


app = Flask(__name__)


@app.route("/validate", methods=["GET"])
def validate():
    requested_path = request.headers.get("X-Original-URI", "/").replace(
        "/restricted/", ""
    )

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        status, message = validate_token(token, requested_path)
        if status == 200:
            return message, status
        else:
            abort(status, message)

    else:
        for cookie in request.cookies:
            if cookie.startswith("isimip_access_token"):
                token = request.cookies.get(cookie)
                status, message = validate_token(token, requested_path)
                if status == 200:
                    return message, status
                else:
                    continue

        abort(401, "No valid access token found in cookies.")
