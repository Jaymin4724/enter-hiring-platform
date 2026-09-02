import pytest

from app.core.db import SessionLocal
from app.models import Application
from app.models.application import STAGES

NIL_UUID = "00000000-0000-0000-0000-000000000000"


def _resume_file(name="resume.pdf", content_type="application/pdf"):
    return {"resume": (name, b"%PDF-1.4 fake resume content for tests", content_type)}


def _valid_form(job_id, **overrides):
    data = {
        "name": "Test Candidate",
        "phone": "+91 98765 43210",
        "email": "candidate@example.com",
        "job_id": job_id,
        "note": "Automated test application.",
    }
    data.update(overrides)
    return data


@pytest.fixture
def sample_job_id(client):
    resp = client.get("/jobs")
    jobs = resp.json()
    assert jobs
    return jobs[0]["id"]


@pytest.fixture
def created_application_ids():
    ids = []
    yield ids
    if ids:
        db = SessionLocal()
        try:
            db.query(Application).filter(Application.id.in_(ids)).delete(synchronize_session=False)
            db.commit()
        finally:
            db.close()


def _submit(client, sample_job_id, created_application_ids, **overrides):
    resp = client.post(
        "/applications",
        data=_valid_form(sample_job_id, **overrides),
        files=_resume_file(),
    )
    if resp.status_code == 201:
        created_application_ids.append(resp.json()["id"])
    return resp


def test_submit_application_success(client, sample_job_id, created_application_ids):
    resp = _submit(client, sample_job_id, created_application_ids)
    assert resp.status_code == 201
    body = resp.json()
    assert body["stage"] == "Applied"
    assert body["job_id"] == sample_job_id
    assert body["resume_path"]


def test_submit_missing_required_field(client, sample_job_id, created_application_ids):
    data = _valid_form(sample_job_id)
    del data["name"]
    resp = client.post("/applications", data=data, files=_resume_file())
    assert resp.status_code == 422


def test_submit_invalid_email(client, sample_job_id, created_application_ids):
    resp = _submit(client, sample_job_id, created_application_ids, email="not-an-email")
    assert resp.status_code == 422


def test_submit_invalid_phone(client, sample_job_id, created_application_ids):
    resp = _submit(client, sample_job_id, created_application_ids, phone="abc")
    assert resp.status_code == 422


def test_submit_unknown_job(client, created_application_ids):
    resp = _submit(client, NIL_UUID, created_application_ids)
    assert resp.status_code == 404


def test_submit_rejects_bad_file_type(client, sample_job_id, created_application_ids):
    resp = client.post(
        "/applications",
        data=_valid_form(sample_job_id),
        files={"resume": ("resume.exe", b"not a resume", "application/x-msdownload")},
    )
    assert resp.status_code == 422


def test_list_applications_requires_auth(client):
    resp = client.get("/applications")
    assert resp.status_code == 401


def test_filter_by_job_and_stage(client, sample_job_id, created_application_ids, auth_headers):
    submit_resp = _submit(client, sample_job_id, created_application_ids)
    application_id = submit_resp.json()["id"]

    by_job = client.get(f"/applications?job_id={sample_job_id}", headers=auth_headers)
    assert by_job.status_code == 200
    assert any(a["id"] == application_id for a in by_job.json())

    by_stage = client.get("/applications?stage=Applied", headers=auth_headers)
    assert any(a["id"] == application_id for a in by_stage.json())

    by_wrong_stage = client.get("/applications?stage=Approved", headers=auth_headers)
    assert all(a["id"] != application_id for a in by_wrong_stage.json())


def test_stage_update_accepts_every_valid_stage(client, sample_job_id, created_application_ids, auth_headers):
    submit_resp = _submit(client, sample_job_id, created_application_ids)
    application_id = submit_resp.json()["id"]

    for stage in STAGES:
        resp = client.patch(f"/applications/{application_id}/stage", json={"stage": stage}, headers=auth_headers)
        assert resp.status_code == 200, resp.text
        assert resp.json()["stage"] == stage


def test_stage_update_rejects_invalid_stage(client, sample_job_id, created_application_ids, auth_headers):
    submit_resp = _submit(client, sample_job_id, created_application_ids)
    application_id = submit_resp.json()["id"]

    resp = client.patch(f"/applications/{application_id}/stage", json={"stage": "Not A Stage"}, headers=auth_headers)
    assert resp.status_code == 422


def test_stage_update_requires_auth(client, sample_job_id, created_application_ids):
    submit_resp = _submit(client, sample_job_id, created_application_ids)
    application_id = submit_resp.json()["id"]

    resp = client.patch(f"/applications/{application_id}/stage", json={"stage": "R1"})
    assert resp.status_code == 401


def test_resume_url_requires_auth(client, sample_job_id, created_application_ids):
    submit_resp = _submit(client, sample_job_id, created_application_ids)
    application_id = submit_resp.json()["id"]

    resp = client.get(f"/applications/{application_id}/resume")
    assert resp.status_code == 401


def test_resume_url_returned_for_admin(client, sample_job_id, created_application_ids, auth_headers):
    submit_resp = _submit(client, sample_job_id, created_application_ids)
    application_id = submit_resp.json()["id"]

    resp = client.get(f"/applications/{application_id}/resume", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["url"]
