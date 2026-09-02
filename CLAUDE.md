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
- Frontend: React + Vite, Tailwind CSS v4, shadcn/ui (Radix base) (`frontend/`)
- Database + file storage: Supabase (Postgres + Storage)
- Hosting: frontend → Vercel, backend → Render, data → Supabase

## Design system

One unified palette across both the public and admin surfaces (not two different ones) — see `docs/PROGRESS.md` Phase 5 for the rationale. Tokens live in `frontend/src/index.css` as CSS variables (`--primary`, `--accent`, `--destructive`, `--muted`, etc., mapped into Tailwind via `@theme inline`) plus custom `--color-stage-*` tokens for the 9 hiring-pipeline stages (neutral → blue → indigo → violet → green progression, red for every Reject variant). Font is Inter throughout. When building admin UI (stage pills, filters), reuse the `--color-stage-*` tokens rather than inventing new colors per stage.

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
cp .env.example .env   # VITE_API_URL, defaults to http://localhost:8000
npm run dev        # Vite dev server
npm run build       # production build
npm run lint         # oxlint
npm run preview
```
Adding a shadcn/ui component: `npx shadcn@latest add <component>` (writes to `src/components/ui/`). No automated frontend test suite — verified manually per `docs/TEST.md`.

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
- `/` → `pages/ApplyPage.jsx` — public application form. Fully working: loads jobs from `GET /jobs`, submits to `POST /applications` via `lib/api.js`, client-side validation mirrors the backend's rules.
- `/admin/login` → `pages/AdminLogin.jsx` — placeholder, not built yet (Phase 6).
- `/admin` → `pages/AdminDashboard.jsx` — placeholder, not built yet (Phase 6/7).

There is one frontend origin and one backend origin — the admin dashboard is not a separate deployable app, just routes gated behind the login flow once auth is implemented.

- `lib/api.js` — fetch wrapper (`getJobs`, `submitApplication`), reads `VITE_API_URL`, parses FastAPI's error-detail shape (including validation-error arrays) into a plain message.
- `lib/utils.js` — shadcn's `cn()` helper (clsx + tailwind-merge).
- `components/ui/` — shadcn-generated primitives (`button`, `input`, `label`, `textarea`, `select`, `card` so far). Add more via `npx shadcn@latest add <name>`, don't hand-write these.
- `components/` (non-`ui/`) — hand-built, product-specific components, e.g. `ResumeDropzone.jsx` (drag-and-drop file upload; shadcn has no primitive for this).

## Secrets

`backend/.env` and any `frontend/.env*` (other than `.env.example`) are gitignored and must never be committed. Supabase keys and the `DATABASE_URL` connection string live only in `backend/.env` locally and in Render/Vercel environment variable settings in production.
