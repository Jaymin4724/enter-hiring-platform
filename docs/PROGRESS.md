# PROGRESS.md

Running summary of decisions made and phases completed. Detailed per-phase plans live in `docs/PLAN.md` (current phase only) — this file is the durable record after each phase's detail is truncated.

## Decisions

- 2026-09-02 — Stack chosen: Python/FastAPI backend, React (Vite) frontend, Supabase (Postgres + Storage) for data and resumes.
- 2026-09-02 — Hosting chosen: frontend on Vercel, backend on Render, Supabase for DB/storage.
- 2026-09-02 — Doc structure set: `REQUIREMENTS.md` → `PRODUCT_VISION.md` → `ROADMAP.md` → `PLAN.md` (current phase, replaced each phase) → `PROGRESS.md` (this file). All docs live in `docs/`, except `CLAUDE.md` which stays at repo root.
- 2026-09-02 — GitHub repo created: [Jaymin4724/enter-hiring-platform](https://github.com/Jaymin4724/enter-hiring-platform) (private). Local `main` pushed and tracking `origin/main`.

## Phases completed

### Phase 1 — Project Scaffolding & Environment Setup (mostly done)

- Git repo initialized at project root, initial commit made.
- `backend/` — FastAPI app scaffolded: venv, dependencies installed, `app/main.py` with CORS + `/health`, `app/core/config.py` for env-based settings. Verified `uvicorn app.main:app` runs and `/health` returns `200 {"status":"ok"}`.
- `frontend/` — React app scaffolded via Vite (`npm create vite@latest -- --template react`), `react-router-dom` installed, placeholder routes wired for `/` (apply page), `/admin/login`, `/admin` (dashboard). Verified `npm run dev` runs.
- `.env.example` added for both backend and frontend; `.gitignore` confirmed to exclude `venv/`, `node_modules/`, and all `.env` files.

**Still open before Phase 1 can close**: a real Supabase project needs to be created and its URL/keys/DB connection string added to `backend/.env` (not committed). This requires the user's Supabase account — see next step.
