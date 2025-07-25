import os
from datetime import UTC, datetime, timedelta

import jwt


def encode_token(subject, path):
    secret = os.getenv("ISIMIP_FILES_AUTH_SECRET")
    if secret is None:
        raise RuntimeError("ISIMIP_FILES_AUTH_SECRET is not set")

    ttl = os.getenv("ISIMIP_FILES_AUTH_TTL", "86400")

    sanitized_path = path.rstrip("/") + "/"

    payload = {
        "sub": subject,
        "exp": datetime.now(UTC) + timedelta(seconds=int(ttl)),
        "iat": datetime.now(UTC),
        "path": sanitized_path,
    }

    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token):
    secret = os.getenv("ISIMIP_FILES_AUTH_SECRET")
    return jwt.decode(token, secret, algorithms=["HS256"])
