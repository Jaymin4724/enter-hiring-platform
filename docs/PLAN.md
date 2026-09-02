# PLAN.md

Detailed plan for the **current phase only**. Replaced entirely when this phase is done — see `docs/ROADMAP.md` for the full phase list, `docs/PROGRESS.md` for what's already done, and `docs/TEST.md` for the test requirements this phase must satisfy before it's marked complete.

## Phase 4 — Backend API: Applications

### Goal
Candidates can submit an application (with resume) through the API, and the admin can list/filter/move them through the stage pipeline. Tests are written alongside each endpoint, not after.

### Tasks

- [ ] `app/schemas/application.py` — `ApplicationOut`, `StageUpdate` (single `stage` field, validated against `STAGES`)
- [ ] `app/services/storage.py` — extend with `upload_resume(file, application_id)` that uploads to the `resumes` bucket and returns the stored path
- [ ] `app/api/applications.py` router:
  - [ ] `POST /applications` — public, multipart form (name, phone, email, resume file, job_id, note), validates job_id exists, uploads resume, creates the row with stage `"Applied"`
  - [ ] `GET /applications` — admin-only, optional `job_id` and `stage` query filters
  - [ ] `PATCH /applications/{id}/stage` — admin-only, body `{ "stage": "..." }`, 400 if not one of the 9 valid stages
  - [ ] `GET /applications/{id}/resume` — admin-only, returns a signed URL (or redirect) to the resume in the private bucket
- [ ] Wire router into `app/main.py`
- [ ] `backend/tests/test_applications.py` — cover every unchecked box under "Phase 4" in `docs/TEST.md`:
  - [ ] submit succeeds, stage defaults to Applied
  - [ ] submit rejects missing required field
  - [ ] submit rejects invalid email
  - [ ] resume ends up in storage, path stored on the row
  - [ ] list requires auth
  - [ ] filter by job_id
  - [ ] filter by stage
  - [ ] stage update accepts each of the 9 stages
  - [ ] stage update rejects an invalid value
  - [ ] tests clean up any application/job/resume they create
- [ ] Run `./venv/Scripts/python -m pytest -v`, confirm everything (Phase 3 + Phase 4 tests) passes
- [ ] Update `docs/TEST.md` — check off the Phase 4 boxes once their tests are green

### Exit criteria
- All Phase 4 boxes in `docs/TEST.md` are checked and the full pytest suite passes.
- A resume file uploaded through `POST /applications` is retrievable by an admin.
- No frontend work yet — that starts in Phase 5.
