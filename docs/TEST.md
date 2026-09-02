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
Automated in `backend/tests/test_applications.py` (13 tests, all passing):
- [x] Public submit-application endpoint accepts a valid payload + resume file, stage defaults to `"Applied"`
- [x] Submit rejects a missing required field
- [x] Submit rejects an invalid email format
- [x] Submit rejects an invalid phone format
- [x] Submit rejects an unknown `job_id` (404)
- [x] Submit rejects a disallowed resume file type
- [x] Resume file lands in the Supabase `resumes` bucket and its path is stored on the row
- [x] Admin list-applications endpoint returns 401 without a token
- [x] Admin can filter applications by `job_id`
- [x] Admin can filter applications by `stage`
- [x] Stage-update endpoint accepts every value in the 9-stage list and persists it
- [x] Stage-update endpoint rejects a value outside the 9-stage list
- [x] Stage-update and resume-URL endpoints both return 401 without a token

### Phase 5 — Frontend: Public Application Page
Manual, in-browser (via claude-in-chrome):
- [x] Job dropdown loads real jobs from the API — confirmed all 10 seeded jobs appear
- [x] Submitting a valid application shows the success state — confirmed, and cross-checked the row landed correctly via `GET /applications` (right job, stage `Applied`, resume path set)
- [x] Missing/invalid field shows an inline validation error, not a silent failure — confirmed empty-submit shows all 4 required-field errors, no request sent
- [x] Resume upload works end to end — file uploaded via the dropzone, submitted, and verified present via the admin API (cleaned up afterward as test data)
- [ ] True small-viewport (mobile) check — window resize in this environment didn't reliably narrow the render viewport, so this is unverified by screenshot. The responsive Tailwind classes (`grid-cols-1 sm:grid-cols-2`, `max-w-xl`, `px-4`) are standard and compiled correctly, but treat this as still open until checked on an actual narrow device/emulator.

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
