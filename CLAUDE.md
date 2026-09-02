# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A candidate application and hiring management system ("enter" — AI Fullstack Intern technical assignment). Two front-ends against one backend:

- **Public application page** — no login, candidates apply to a job picked from a dropdown.
- **Admin dashboard** — `admin@enter.in` login only, manages jobs and moves applications through a fixed hiring pipeline (Applied → R1/R1 Reject → R2/R2 Reject → R3/R3 Reject → Approved, or Reject at any point).

Full spec, product vision, phase roadmap, current-phase plan, and decision log all live in `docs/` — read them before making product or architecture decisions:

- `docs/REQUIREMENTS.md` — the assignment spec, translated into requirements.
- `docs/PRODUCT_VISION.md` — what the two front-ends should look and feel like.
- `docs/ROADMAP.md` — the full list of build phases and the stack/hosting decision.
- `docs/PLAN.md` — **detailed plan for the current phase only**. It is replaced wholesale when a phase finishes (do not expect history here).
- `docs/PROGRESS.md` — durable summary of decisions made and phases completed so far. Check this first to know what already exists before re-deriving it from code.
- `docs/TEST.md` — phase-by-phase test requirements (automated backend tests + manual frontend checklist). Write/extend tests alongside a phase's code, not after.

## Stack

- Backend: Python, FastAPI (`backend/`)
- Frontend: React + Vite (`frontend/`)
- Database + file storage: Supabase (Postgres + Storage)
- Hosting: frontend → Vercel, backend → Render, data → Supabase

## Commands

### Backend (`backend/`)
```
python -m venv venv                          # one-time
./venv/Scripts/pip install -r requirements.txt
cp .env.example .env                          # then fill in Supabase/DB values
./venv/Scripts/python -m uvicorn app.main:app --reload
```
Tests (`backend/tests/`, pytest + FastAPI `TestClient`, run against the real Supabase dev DB — see `docs/TEST.md`):
```
./venv/Scripts/pip install -r requirements-dev.txt   # one-time: pytest + httpx2
./venv/Scripts/python -m pytest -v
```
No linter configured yet.

### Frontend (`frontend/`)
```
npm install
npm run dev        # Vite dev server
npm run build       # production build
npm run lint         # oxlint
npm run preview
```

## Architecture

**Backend** (`backend/app/`) is organized by layer, not by feature:
- `main.py` — FastAPI app instance, CORS middleware (origin from `settings.frontend_origin`), route registration.
- `core/config.py` — all environment-driven settings (Supabase URL/keys, `DATABASE_URL`, auth secret, frontend origin) via `pydantic-settings`, loaded from `backend/.env`.
- `api/` — routers (`auth.py`, `jobs.py`, `applications.py`), one file per resource, registered in `main.py` via `include_router`.
- `models/` — SQLAlchemy models (`Job`, `Application`, `Admin`), declared against `models/base.py`'s `Base`; `core/db.py` holds the engine/session (`get_db` dependency). `models/application.py` also holds `STAGES` (the 9-value hiring pipeline list) and `DEFAULT_STAGE` — the single source of truth for valid stage values, imported by both the schema validator and any code checking a stage.
- `schemas/` — Pydantic request/response models, one file per resource, imported by the matching router.
- `services/` — business logic that isn't pure routing: `services/auth.py` (password check, JWT create/decode, `get_current_admin` dependency), `services/storage.py` (Supabase Storage: `upload_resume` with content-type/size validation, `get_resume_signed_url`, `delete_resume`, `ensure_resume_bucket`).
When adding a resource, follow this same split rather than putting logic directly in `main.py`.

Data access is direct to the Supabase Postgres instance via `DATABASE_URL` (SQLAlchemy/psycopg2), not through the Supabase REST client — the `supabase` Python package is used for Storage (resume uploads) and any auth-adjacent calls, not as the primary DB layer.

**Frontend** (`frontend/src/`) is a single Vite React app covering both public and admin surfaces, split by route in `App.jsx` via `react-router-dom`:
- `/` → `pages/ApplyPage.jsx` — public application form.
- `/admin/login` → `pages/AdminLogin.jsx`.
- `/admin` → `pages/AdminDashboard.jsx` — jobs + candidates management.

There is one frontend origin and one backend origin — the admin dashboard is not a separate deployable app, just routes gated behind the login flow once auth is implemented.

## Secrets

`backend/.env` and any `frontend/.env*` (other than `.env.example`) are gitignored and must never be committed. Supabase keys and the `DATABASE_URL` connection string live only in `backend/.env` locally and in Render/Vercel environment variable settings in production.
