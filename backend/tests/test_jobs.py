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


def test_create_job_rejects_blank_title(client, auth_headers):
    resp = client.post("/jobs", json={"title": "   "}, headers=auth_headers)
    assert resp.status_code == 422


def test_create_job_rejects_title_over_max_length(client, auth_headers):
    resp = client.post("/jobs", json={"title": "A" * 201}, headers=auth_headers)
    assert resp.status_code == 422


def test_create_job_rejects_department_over_max_length(client, auth_headers):
    resp = client.post("/jobs", json={"title": "Valid Title", "department": "A" * 121}, headers=auth_headers)
    assert resp.status_code == 422


def test_create_job_rejects_description_over_max_length(client, auth_headers):
    resp = client.post("/jobs", json={"title": "Valid Title", "description": "A" * 5001}, headers=auth_headers)
    assert resp.status_code == 422


def test_create_job_rejects_location_over_max_length(client, auth_headers):
    resp = client.post("/jobs", json={"title": "Valid Title", "location": "A" * 121}, headers=auth_headers)
    assert resp.status_code == 422


def test_create_job_trims_whitespace(client, auth_headers):
    create_resp = client.post(
        "/jobs",
        json={"title": "  Trimmed Title  ", "department": "  Eng  ", "location": "   ", "description": None},
        headers=auth_headers,
    )
    assert create_resp.status_code == 201
    body = create_resp.json()
    assert body["title"] == "Trimmed Title"
    assert body["department"] == "Eng"
    assert body["location"] is None
    client.delete(f"/jobs/{body['id']}", headers=auth_headers)


def test_create_job_with_only_title_succeeds(client, auth_headers):
    create_resp = client.post("/jobs", json={"title": "Title-Only Job"}, headers=auth_headers)
    assert create_resp.status_code == 201
    body = create_resp.json()
    assert body["title"] == "Title-Only Job"
    assert body["department"] is None
    assert body["location"] is None
    assert body["description"] is None
    client.delete(f"/jobs/{body['id']}", headers=auth_headers)


def test_update_job_rejects_blank_title(client, auth_headers):
    create_resp = client.post("/jobs", json={"title": "Job To Update"}, headers=auth_headers)
    job_id = create_resp.json()["id"]
    try:
        update_resp = client.put(f"/jobs/{job_id}", json={"title": "   "}, headers=auth_headers)
        assert update_resp.status_code == 422
    finally:
        client.delete(f"/jobs/{job_id}", headers=auth_headers)


def test_update_job_rejects_title_over_max_length(client, auth_headers):
    create_resp = client.post("/jobs", json={"title": "Job To Update"}, headers=auth_headers)
    job_id = create_resp.json()["id"]
    try:
        update_resp = client.put(f"/jobs/{job_id}", json={"title": "A" * 201}, headers=auth_headers)
        assert update_resp.status_code == 422
    finally:
        client.delete(f"/jobs/{job_id}", headers=auth_headers)


def test_update_job_trims_whitespace(client, auth_headers):
    create_resp = client.post("/jobs", json={"title": "Job To Update"}, headers=auth_headers)
    job_id = create_resp.json()["id"]
    try:
        update_resp = client.put(
            f"/jobs/{job_id}",
            json={"title": "  Updated Title  ", "department": "  Ops  "},
            headers=auth_headers,
        )
        assert update_resp.status_code == 200
        body = update_resp.json()
        assert body["title"] == "Updated Title"
        assert body["department"] == "Ops"
    finally:
        client.delete(f"/jobs/{job_id}", headers=auth_headers)


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
