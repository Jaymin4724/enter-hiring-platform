# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A candidate application and hiring management system ("enter" — AI Fullstack Intern technical assignment). Two front-ends against one backend:

- **Public application page** — no login, candidates apply to a job picked from a dropdown.
- **Admin dashboard** — `admin@enter.in` login only, manages jobs and moves applications through a fixed hiring pipeline (Applied → R1/R1 Reject → R2/R2 Reject → R3/R3 Reject → Approved, or Reject at any point).

`README.md` at the repo root is the interviewer-facing overview (stack + why, architecture, key decisions, how to run it, live links once deployed) — keep it in sync whenever a decision or the project's state changes, same as this file.

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

One-off scripts at the backend root (`create_tables.py`, `setup_storage.py`, `seed.py`, `seed_demo_candidates.py`) — not part of the app package, run directly against whatever `DATABASE_URL`/Supabase project `.env` points at. `seed_demo_candidates.py` generates realistic resume PDFs (`fpdf2`, dev-only dependency) and submits 10 fake candidates through the real API so the admin dashboard has believable demo data; output goes to gitignored `backend/seed_data/`.

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

**Frontend** (`frontend/src/`) is a single Vite React app covering both public and admin surfaces, split by route in `App.jsx` via `react-router-dom` (nested routes for `/admin/*`):
- `/` → `pages/ApplyPage.jsx` — public application form. Fully working: loads jobs from `GET /jobs`, submits to `POST /applications` via `lib/api.js`, client-side validation mirrors the backend's rules.
- `/admin/login` → `pages/AdminLogin.jsx` — working login, calls `lib/api.js`'s `login()`, stores the token via `lib/auth.js`.
- `/admin` → guarded by `components/RequireAuth.jsx` (redirects to `/admin/login` if no token), renders `pages/AdminDashboard.jsx` as a layout (top nav + `<Outlet />`) with nested routes:
  - `/admin/jobs` → `pages/admin/JobsPage.jsx` — fully working jobs CRUD (table, `Sheet` slide-over for create/edit, `AlertDialog` for delete).
  - `/admin/candidates` → `pages/admin/CandidatesPage.jsx` — fully working: job/stage filters, per-row stage change (the pill *is* the `Select`, styled via `lib/stages.js`'s `stageBadgeClass`), resume links fetched lazily on click via a signed URL.

Small nav conveniences (explicitly requested, not in the original spec): an "Admin login" link on `ApplyPage`, "Back to Home" on `AdminLogin`, and a "Home" button in the admin top nav — plain `react-router` `Link`s, nothing fancier.

There is one frontend origin and one backend origin — the admin dashboard is not a separate deployable app, just routes gated behind the login flow.

- `lib/api.js` — fetch wrapper built around a shared `request()` helper; admin calls pass `auth: true` to attach the bearer token automatically. `getJobs`, `submitApplication`, `login`, `createJob`, `updateJob`, `deleteJob`, `getApplications`, `updateApplicationStage`, `getResumeUrl`. Parses FastAPI's error-detail shape (including validation-error arrays) into a plain message.
- `lib/auth.js` — token storage (`localStorage` — acceptable for this internal tool; the public page never touches it). `getToken`/`setToken`/`clearToken`/`isAuthenticated`.
- `lib/stages.js` — frontend's single source of truth for the 9 hiring stages (must match `backend/app/models/application.py`'s `STAGES` exactly) plus `stageBadgeClass(stage)` mapping a stage to its `--color-stage-*` token pair. Use this anywhere a stage needs to be listed or colored — don't redeclare the stage list or hardcode colors elsewhere.
- `lib/utils.js` — shadcn's `cn()` helper (clsx + tailwind-merge).
- `components/ui/` — shadcn-generated primitives (`button`, `input`, `label`, `textarea`, `select`, `card`, `table`, `badge`, `sheet`, `alert-dialog` so far). Add more via `npx shadcn@latest add <name>`, don't hand-write these. Note: shadcn's `Table` already wraps itself in `overflow-x-auto` — don't add another wrapper.
- `components/` (non-`ui/`) — hand-built, product-specific components: `ResumeDropzone.jsx` (drag-and-drop file upload; shadcn has no primitive for this), `RequireAuth.jsx` (route guard).
- Touch targets: admin row action buttons are `h-10 w-10` (40px) rather than shadcn's smaller default icon-button size — keep new icon-only buttons at least that size.

## Deployment

`render.yaml` at the repo root is a Render Blueprint for the backend (root dir `backend`, build/start commands, required env vars listed with `sync: false` so secrets are entered once in the Render dashboard, never committed). Vercel needs no config file for the frontend — set Root Directory to `frontend` in its dashboard, it auto-detects Vite. See `docs/PLAN.md` (Phase 8) for the full deploy sequence — note the two-step dependency: the backend's `FRONTEND_ORIGIN` can't be set to the real value until the frontend is deployed and has a URL, and the frontend's `VITE_API_URL` can't be set until the backend does.

## Secrets

`backend/.env` and any `frontend/.env*` (other than `.env.example`) are gitignored and must never be committed. Supabase keys and the `DATABASE_URL` connection string live only in `backend/.env` locally and in Render/Vercel environment variable settings in production.
