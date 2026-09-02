# PROGRESS.md

Running summary of decisions made and phases completed. Detailed per-phase plans live in `docs/PLAN.md` (current phase only) — this file is the durable record after each phase's detail is truncated.

## Decisions

- 2026-09-02 — Stack chosen: Python/FastAPI backend, React (Vite) frontend, Supabase (Postgres + Storage) for data and resumes.
- 2026-09-02 — Hosting chosen: frontend on Vercel, backend on Render, Supabase for DB/storage.
- 2026-09-02 — Doc structure set: `REQUIREMENTS.md` → `PRODUCT_VISION.md` → `ROADMAP.md` → `PLAN.md` (current phase, replaced each phase) → `PROGRESS.md` (this file). All docs live in `docs/`, except `CLAUDE.md` which stays at repo root.
- 2026-09-02 — GitHub repo created: [Jaymin4724/enter-hiring-platform](https://github.com/Jaymin4724/enter-hiring-platform) (private). Local `main` pushed and tracking `origin/main`.

## Phases completed

### Phase 1 — Project Scaffolding & Environment Setup

- Git repo initialized at project root, initial commit made.
- `backend/` — FastAPI app scaffolded: venv, dependencies installed, `app/main.py` with CORS + `/health`, `app/core/config.py` for env-based settings. Verified `uvicorn app.main:app` runs and `/health` returns `200 {"status":"ok"}`.
- `frontend/` — React app scaffolded via Vite (`npm create vite@latest -- --template react`), `react-router-dom` installed, placeholder routes wired for `/` (apply page), `/admin/login`, `/admin` (dashboard). Verified `npm run dev` runs.
- `.env.example` added for both backend and frontend; `.gitignore` confirmed to exclude `venv/`, `node_modules/`, and all `.env` files.

- Supabase project created by the user (ref `caicygijzymwkbldjrnb`). `backend/.env` filled in with real `SUPABASE_URL`, anon key, service role key, and `DATABASE_URL`; a `SUPABASE_URL` copy-paste error (stray `/rest/v1/` path) was fixed. Direct Postgres connection verified working (`psycopg2` connect + `SELECT version()` succeeded, Postgres 17.6). `AUTH_SECRET_KEY` placeholder replaced with a generated random secret.

**Phase 1 is complete.**

### Phase 2 — Supabase Schema & Storage Setup

- SQLAlchemy models added: `app/models/job.py` (`Job`), `app/models/application.py` (`Application`, plus the 9-stage `STAGES` list), `app/models/admin.py` (`Admin`). UUID primary keys, `app/core/db.py` holds the engine/session.
- Tables created directly with `Base.metadata.create_all()` via a one-off `backend/create_tables.py` script — no Alembic. Decision: not worth the migration-tooling overhead for a single-shot schema on a 24h build; revisit only if the schema needs to evolve after data exists.
- Private `resumes` bucket created in Supabase Storage via `app/services/storage.py` (`ensure_resume_bucket()`, run once via `backend/setup_storage.py`).
- Seed script `backend/seed.py` run against the real Supabase DB: 10 jobs inserted, 1 admin inserted. Verified via row counts (`jobs: 10`, `admins: 1`) — confirmed no duplicates.
- **Admin login for submission**: email `admin@enter.in`, password `Enter@Hiring2026`.
- Dependency swap: `passlib[bcrypt]` was in the original Phase 1 requirements list but its bcrypt backend detection is broken with the currently-installed `bcrypt` (4.x) — a known passlib/bcrypt compatibility issue. Switched to calling `bcrypt.hashpw`/`bcrypt.checkpw` directly (see `backend/seed.py`); `requirements.txt` updated to drop `passlib` in favor of plain `bcrypt`. Use `bcrypt` directly again for login verification in Phase 3, not passlib.

**Phase 2 is complete.**

### Phase 3 — Backend API: Auth & Jobs

- Schemas added: `app/schemas/job.py` (`JobCreate`/`JobUpdate`/`JobOut`), `app/schemas/auth.py` (`LoginRequest`/`TokenResponse`, using `EmailStr` — required adding `email-validator` to `requirements.txt`).
- `app/services/auth.py`: password check via `bcrypt` directly (consistent with the Phase 2 passlib swap), JWT create/decode, `get_current_admin` FastAPI dependency (bearer token).
- Library decision: used **PyJWT**, not `python-jose` (which was in the original Phase 1 plan). Checked current guidance — FastAPI's own docs have moved off `python-jose` due to maintenance/security concerns, PyJWT is the actively maintained choice. `requirements.txt` updated accordingly.
- Routers: `app/api/auth.py` (`POST /auth/login`), `app/api/jobs.py` (`GET /jobs` public, `POST`/`PUT /{id}`/`DELETE /{id}` admin-only via `get_current_admin`). Both wired into `app/main.py`.
- Testing: added a real pytest suite (`backend/tests/`, `TestClient`, run against the live Supabase dev DB) instead of only manual curl checks — see `docs/TEST.md` for the phase-by-phase test plan going forward. `backend/requirements-dev.txt` added for `pytest` + `httpx2` (not plain `httpx` — Starlette's TestClient now deprecates it in favor of `httpx2`). All 9 tests pass: login success/wrong-password/unknown-email, public `GET /jobs`, auth-required checks on create/update/delete, and a full create→update→delete lifecycle that cleans up after itself.
- Manually verified against the live API too: login returns a token, `GET /jobs` returns the 10 seeded jobs with no auth, unauthenticated writes return 401.

**Phase 3 is complete.**

### Phase 4 — Backend API: Applications

- `app/schemas/application.py`: `ApplicationOut`, `StageUpdate` (validates against the 9-stage list from `app/models/application.py`).
- `app/services/storage.py` extended: `upload_resume()` (validates content type against PDF/DOC/DOCX, 5MB size cap, uploads to the private `resumes` bucket), `get_resume_signed_url()`, `delete_resume()`.
- `app/api/applications.py`: `POST /applications` (public, multipart — validates email via `email_validator`, phone via regex, resume type/size; 404 on unknown job), `GET /applications` (admin-only, `job_id`/`stage` filters), `PATCH /applications/{id}/stage` (admin-only), `GET /applications/{id}/resume` (admin-only, signed URL). Wired into `app/main.py`.
- Fixed a real deprecation warning surfaced during test runs: `status.HTTP_422_UNPROCESSABLE_ENTITY` is deprecated in current Starlette in favor of `HTTP_422_UNPROCESSABLE_CONTENT` — swapped across `applications.py`.
- Testing: `backend/tests/test_applications.py`, 13 tests, all passing — covers valid submit, every validation failure path (missing field, bad email, bad phone, unknown job, bad file type), auth-gating on all three admin endpoints, job/stage filtering, and every one of the 9 stage values accepted plus an invalid one rejected. Full suite is now 22 tests, all green. Test applications clean up their own DB rows via a fixture teardown (resume files in Storage are not cleaned up per test — acceptable for a 24h build, noted here rather than silently left undocumented).

**Phase 4 is complete.**
