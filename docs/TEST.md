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

## Validation checklist (client + admin)

Every rule below is enforced **server-side** (the real source of truth) and **mirrored client-side** (fast feedback, no round trip for the obvious cases). Server-side is what the automated tests in Phase 3/4/6 above actually check; client-side is verified manually in the browser.

### Client side — public application form (`POST /applications`)

| Field | Rule | Server (backend) | Client (`ApplyPage.jsx`) |
|---|---|---|---|
| Name | required, non-blank after trim, ≤200 chars | ✅ `app/api/applications.py` | ✅ `validate()` + `maxLength={200}` |
| Phone | required, matches `^\+?[0-9 ()-]{7,20}$` | ✅ | ✅ same pattern |
| Email | required, valid format (`email_validator`) | ✅ | ✅ regex mirror |
| Job | required, must reference an existing job (404 if not) | ✅ | ✅ dropdown only offers real jobs |
| Resume | required, PDF/DOC/DOCX only, ≤5MB | ✅ `services/storage.py` | ✅ dropzone + `validate()` |
| Note | optional, ≤2000 chars | ✅ | ✅ `maxLength={2000}` |

### Admin side — jobs management (`POST /jobs`, `PUT /jobs/{id}`)

| Field | Rule | Server (backend) | Client (`admin/JobsPage.jsx`) |
|---|---|---|---|
| Title | required, non-blank after trim, ≤200 chars | ✅ `schemas/job.py` (`JobWrite`) | ✅ inline error + `maxLength={200}` |
| Department | optional, ≤120 chars | ✅ | ✅ `maxLength={120}` |
| Location | optional, ≤120 chars | ✅ | ✅ `maxLength={120}` |
| Description | optional, ≤5000 chars (DB column is unbounded `Text`, capped anyway) | ✅ | ✅ `maxLength={5000}` |

### Admin side — login (`POST /auth/login`)

| Check | Server | Client |
|---|---|---|
| Wrong password / unknown email → 401, generic message (no user enumeration) | ✅ | ✅ shown inline on the login form |
| Stage value must be one of the 9 valid stages (`PATCH /applications/{id}/stage`) | ✅ `schemas/application.py` | ✅ the row Select in `CandidatesPage.jsx` only ever offers the 9 valid values, no free text |

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
Automated in `backend/tests/test_auth.py`, `backend/tests/test_jobs.py` (17 tests, all passing):
- [x] `POST /auth/login` succeeds with the seeded admin credentials, returns a bearer token
- [x] `POST /auth/login` returns 401 on wrong password
- [x] `POST /auth/login` returns 401 on unknown email
- [x] `GET /jobs` works with no auth and returns the seeded jobs
- [x] `POST /jobs` returns 401 without a token
- [x] `PUT /jobs/{id}` returns 401 without a token
- [x] `DELETE /jobs/{id}` returns 401 without a token
- [x] Full authenticated lifecycle: create a job → it appears in `GET /jobs` → update it → delete it → it's gone from `GET /jobs`
- [x] Create/update rejects a blank (whitespace-only) title
- [x] Create/update rejects a title over 200 characters
- [x] Create rejects a department over 120 characters
- [x] Create rejects a location over 120 characters
- [x] Create rejects a description over 5000 characters
- [x] Create/update trims surrounding whitespace from title/department/location before storing
- [x] Create succeeds with only a title (department/location/description all optional)

### Phase 4 — Backend API: Applications
Automated in `backend/tests/test_applications.py` (17 tests, all passing):
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
- [x] Submit rejects a whitespace-only name
- [x] Submit rejects a name over 200 characters
- [x] Submit rejects a note over 2000 characters
- [x] Submit trims surrounding whitespace from name/phone/email before storing

### Phase 5 — Frontend: Public Application Page
Manual, in-browser (via claude-in-chrome):
- [x] Job dropdown loads real jobs from the API — confirmed all 10 seeded jobs appear
- [x] Submitting a valid application shows the success state — confirmed, and cross-checked the row landed correctly via `GET /applications` (right job, stage `Applied`, resume path set)
- [x] Missing/invalid field shows an inline validation error, not a silent failure — confirmed empty-submit shows all 4 required-field errors, no request sent
- [x] Resume upload works end to end — file uploaded via the dropzone, submitted, and verified present via the admin API (cleaned up afterward as test data)
- [ ] True small-viewport (mobile) check — window resize in this environment didn't reliably narrow the render viewport, so this is unverified by screenshot. The responsive Tailwind classes (`grid-cols-1 sm:grid-cols-2`, `max-w-xl`, `px-4`) are standard and compiled correctly, but treat this as still open until checked on an actual narrow device/emulator.

### Phase 6 — Frontend: Admin Dashboard (Login & Jobs)
Manual, in-browser:
- [x] Wrong credentials show an error on the login screen
- [x] Correct credentials reach the dashboard
- [x] Visiting `/admin` while logged out redirects to `/admin/login`
- [x] Create/edit/delete a job from the UI is reflected immediately in the list — verified with a real test job, cleaned up, confirmed no leftovers via a direct API check
- [x] Jobs table scrolls horizontally on narrow screens instead of breaking layout (shadcn `Table` wraps itself in `overflow-x-auto` — confirmed by reading the component)
- [x] Edit/Delete icon buttons are touch-target sized (40x40px, up from shadcn's 32px default)

### Phase 7 — Frontend: Admin Dashboard (Candidates)
Manual, in-browser (verified against the 10 real seeded demo candidates):
- [x] Candidates table shows every field captured on the public form (name, email, phone, job, stage, applied date, resume)
- [x] Job filter and stage filter work individually and combined — e.g. stage=R2 alone returned exactly the 2 matching candidates; job=QA Engineer + stage=R2 combined narrowed to exactly 1
- [x] Changing a candidate's stage in the row persists after a page reload — verified on a real candidate, then reverted to its original seeded value afterward (no lasting data change)
- [x] Resume link/download works from the row — opens a real, working signed Supabase Storage URL in a new tab
- [x] Mobile-friendly: same `overflow-x-auto` table pattern as `JobsPage.jsx`, no new fixed-width containers introduced
- [x] Navigation convenience: "Admin login" link on the public page, "Back to Home" on the login screen, "Home" button in the admin nav — all verified working

### Phase 8 — Deployment
Manual, against the hosted URLs:
- [x] Hosted backend responds on `/health` — `https://enter-hiring-platform.onrender.com/health`
- [x] Hosted frontend loads and reaches the hosted backend with no CORS errors — confirmed via `access-control-allow-origin` header check and a real browser submission
- [x] End-to-end: submit an application on the hosted public page, see it appear in the hosted admin dashboard — done with a real resume upload, verified in the live Candidates table, then cleaned up
- [x] Direct navigation to a non-root route (e.g. `/admin/login`) works on the hosted frontend, not just client-side navigation from `/` — this was a real bug (Vercel SPA rewrite), now fixed and verified

### Phase 9 — Seed, QA & Submission
- [x] Full walkthrough of both flows on the hosted links — applied for a job on the live public page (UI/UX Designer, real uploaded resume), confirmed it appeared in the live admin dashboard, moved it Applied → R1 and confirmed the change persisted on re-fetch, confirmed the resume signed URL resolves to a real `application/pdf` (200), then cleaned up
- [x] No console errors on the public page — confirmed via a fresh page load with console tracking armed, zero messages of any kind
- [x] Production DB has the final 10 jobs + 10 demo candidates + 1 admin, no leftover test data — verified via direct API count before and after the walkthrough (10 → 11 → 10)
- [x] `README.md` re-read end to end as a first-time reviewer — fixed one stale line ("Hosting (planned)" left over from before Phase 8 shipped)
