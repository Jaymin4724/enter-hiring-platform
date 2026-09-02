# TEST.md

What gets tested, phase by phase. Checked and updated as each phase in `docs/ROADMAP.md` is built — tests are written alongside the code for that phase, not bolted on afterward.

## Approach

- **Backend**: `pytest` + FastAPI's `TestClient`, in `backend/tests/`, one file per API area (mirrors `backend/app/api/`). Run with:
  ```
  cd backend
  ./venv/Scripts/pip install -r requirements-dev.txt   # pytest + httpx2, one-time
  ./venv/Scripts/python -m pytest -v
  ```
- Tests run against the real Supabase dev database — no mocking, no separate test DB (not worth the setup time for this project). Any test that creates data cleans it up in the same test (see `test_job_crud_lifecycle` for the pattern: create → assert → delete in a `finally`).
- **Frontend**: no automated test suite planned given the timeline. Each frontend phase is verified manually in the browser — checklist items below are marked off by hand, not by a runner.
- A phase isn't "done" in `docs/PROGRESS.md` until the tests below for that phase pass (automated ones actually run green; manual ones actually clicked through).

## Phase-by-phase requirements

### Phase 1 — Scaffolding
No business logic yet, no automated tests warranted.
- [x] Manual: `GET /health` returns `200 {"status":"ok"}`
- [x] Manual: `npm run dev` renders the placeholder routes

### Phase 2 — Supabase Schema & Storage
One-off bootstrap scripts, not runtime code paths — verified manually, not covered by pytest.
- [x] Manual: `jobs`, `applications`, `admins` tables exist with expected columns
- [x] Manual: `resumes` storage bucket exists
- [x] Manual: seed produces exactly 10 jobs and 1 admin, no duplicates on re-run

### Phase 3 — Backend API: Auth & Jobs
Automated in `backend/tests/test_auth.py`, `backend/tests/test_jobs.py`:
- [x] `POST /auth/login` succeeds with the seeded admin credentials, returns a bearer token
- [x] `POST /auth/login` returns 401 on wrong password
- [x] `POST /auth/login` returns 401 on unknown email
- [x] `GET /jobs` works with no auth and returns the seeded jobs
- [x] `POST /jobs` returns 401 without a token
- [x] `PUT /jobs/{id}` returns 401 without a token
- [x] `DELETE /jobs/{id}` returns 401 without a token
- [x] Full authenticated lifecycle: create a job → it appears in `GET /jobs` → update it → delete it → it's gone from `GET /jobs`

### Phase 4 — Backend API: Applications
Planned: `backend/tests/test_applications.py`
- [ ] Public submit-application endpoint accepts a valid payload + resume file, stage defaults to `"Applied"`
- [ ] Submit rejects a missing required field
- [ ] Submit rejects an invalid email format
- [ ] Resume file lands in the Supabase `resumes` bucket and its path is stored on the row
- [ ] Admin list-applications endpoint returns 401 without a token
- [ ] Admin can filter applications by `job_id`
- [ ] Admin can filter applications by `stage`
- [ ] Stage-update endpoint accepts every value in the 9-stage list and persists it
- [ ] Stage-update endpoint rejects a value outside the 9-stage list

### Phase 5 — Frontend: Public Application Page
Manual, in-browser:
- [ ] Job dropdown loads real jobs from the API
- [ ] Submitting a valid application shows the success state
- [ ] Missing/invalid field shows an inline validation error, not a silent failure
- [ ] Resume upload works end to end — file shows up in Storage and is linked from the admin dashboard afterward

### Phase 6 — Frontend: Admin Dashboard (Login & Jobs)
Manual, in-browser:
- [ ] Wrong credentials show an error on the login screen
- [ ] Correct credentials reach the dashboard
- [ ] Visiting `/admin` while logged out redirects to `/admin/login`
- [ ] Create/edit/delete a job from the UI is reflected immediately in the list

### Phase 7 — Frontend: Admin Dashboard (Candidates)
Manual, in-browser:
- [ ] Candidates table shows every field captured on the public form
- [ ] Job filter and stage filter work individually and combined
- [ ] Changing a candidate's stage in the row persists after a page reload
- [ ] Resume link/download works from the row

### Phase 8 — Deployment
Manual, against the hosted URLs:
- [ ] Hosted backend responds on `/health`
- [ ] Hosted frontend loads and reaches the hosted backend with no CORS errors
- [ ] End-to-end: submit an application on the hosted public page, see it appear in the hosted admin dashboard

### Phase 9 — Seed, QA & Submission
- [ ] Full walkthrough of both flows on the hosted links, no console errors
- [ ] Production DB has the final 10 jobs + 1 admin, no leftover test data from development
