import os
from datetime import UTC, datetime, timedelta

import jwt


def validate_token(token, requested_path):
    try:
        payload = decode_token(token)

        token_paths = payload.get("paths")
        if not token_paths:
            return 403, "No paths claim in token"

        if not any(requested_path.startswith(token_path) for token_path in token_paths):
            return 403, "Path not authorized"

        return 200, ""

    except jwt.ExpiredSignatureError:
        return 401, "Token expired"
    except jwt.InvalidTokenError:
        return 401, "Invalid token"


def encode_token(subject, paths):
    secret = os.getenv("ISIMIP_FILES_AUTH_SECRET")
    if secret is None:
        raise RuntimeError("ISIMIP_FILES_AUTH_SECRET is not set")

    ttl = os.getenv("ISIMIP_FILES_AUTH_TTL", "86400")

    sanitized_paths = [path.rstrip("/") + "/" for path in paths]

    payload = {
        "sub": subject,
        "exp": datetime.now(UTC) + timedelta(seconds=int(ttl)),
        "iat": datetime.now(UTC),
        "paths": sanitized_paths,
    }

    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token):
    secret = os.getenv("ISIMIP_FILES_AUTH_SECRET")
    return jwt.decode(token, secret, algorithms=["HS256"])
