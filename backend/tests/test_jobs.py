NIL_UUID = "00000000-0000-0000-0000-000000000000"


def test_list_jobs_is_public(client):
    resp = client.get("/jobs")
    assert resp.status_code == 200
    jobs = resp.json()
    assert len(jobs) >= 10


def test_create_job_requires_auth(client):
    resp = client.post("/jobs", json={"title": "Unauthorized Test Job"})
    assert resp.status_code == 401


def test_update_job_requires_auth(client):
    resp = client.put(f"/jobs/{NIL_UUID}", json={"title": "x"})
    assert resp.status_code == 401


def test_delete_job_requires_auth(client):
    resp = client.delete(f"/jobs/{NIL_UUID}")
    assert resp.status_code == 401


def test_job_crud_lifecycle(client, auth_headers):
    create_resp = client.post(
        "/jobs",
        json={
            "title": "Pytest Temp Job",
            "department": "QA",
            "location": "Remote",
            "description": "Created by an automated test; deleted at the end of the same test.",
        },
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    job_id = create_resp.json()["id"]

    try:
        list_resp = client.get("/jobs")
        assert any(j["id"] == job_id for j in list_resp.json())

        update_resp = client.put(
            f"/jobs/{job_id}",
            json={
                "title": "Pytest Temp Job (Updated)",
                "department": "QA",
                "location": "Remote",
                "description": "Updated by the same test.",
            },
            headers=auth_headers,
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["title"] == "Pytest Temp Job (Updated)"
    finally:
        delete_resp = client.delete(f"/jobs/{job_id}", headers=auth_headers)
        assert delete_resp.status_code == 204

    list_after = client.get("/jobs")
    assert all(j["id"] != job_id for j in list_after.json())
