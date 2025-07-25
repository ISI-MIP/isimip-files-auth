import os

import pytest

from isimip_files_auth.app import app as flask_app
from isimip_files_auth.utils import encode_token


@pytest.fixture
def client():
    flask_app.testing = True
    return flask_app.test_client()


@pytest.fixture(scope="session", autouse=True)
def test_env():
    os.environ["ISIMIP_FILES_AUTH_SECRET"] = "test-secret"


def test_validate_header(client):
    token = encode_token("mail@example.com", "/secure/data")

    response = client.get(
        "/validate",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Original-URI": "/secure/data/path",
        },
    )
    assert response.status_code == 200


def test_validate_header_invalid_token(client):
    token = "invalid"

    response = client.get(
        "/validate",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Original-URI": "/secure/data/path",
        },
    )
    assert response.status_code == 401


def test_validate_header_invalid_path(client):
    token = encode_token("mail@example.com", "/secure/data")

    response = client.get(
        "/validate",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Original-URI": "/secure/invalid",
        },
    )
    assert response.status_code == 403


def test_validate_cookie(client):
    token = encode_token("mail@example.com", "/secure/data")

    client.set_cookie(key="access_token", value=token)

    response = client.get("/validate", headers={"X-Original-URI": "/secure/data/path"})
    assert response.status_code == 200


def test_validate_cookie_invalid_token(client):
    token = "invalid"

    client.set_cookie(key="access_token", value=token)

    response = client.get("/validate", headers={"X-Original-URI": "/secure/data/path"})
    assert response.status_code == 401


def test_validate_cookie_invalid_path(client):
    token = encode_token("mail@example.com", "/secure/data")

    client.set_cookie(key="access_token", value=token)

    response = client.get("/validate", headers={"X-Original-URI": "/secure/invalid"})
    assert response.status_code == 403
