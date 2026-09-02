import pytest
from fastapi.testclient import TestClient

from app.main import app

ADMIN_EMAIL = "admin@enter.in"
ADMIN_PASSWORD = "Enter@Hiring2026"


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    resp = client.post("/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


@pytest.fixture
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
