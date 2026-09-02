from tests.conftest import ADMIN_EMAIL, ADMIN_PASSWORD


def test_login_success(client):
    resp = client.post("/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password(client):
    resp = client.post("/auth/login", json={"email": ADMIN_EMAIL, "password": "wrong-password"})
    assert resp.status_code == 401


def test_login_unknown_email(client):
    resp = client.post("/auth/login", json={"email": "nobody@enter.in", "password": "whatever"})
    assert resp.status_code == 401
