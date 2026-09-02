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
