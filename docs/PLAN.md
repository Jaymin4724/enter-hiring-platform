# PLAN.md

Detailed plan for the **current phase only**. Replaced entirely when this phase is done — see `docs/ROADMAP.md` for the full phase list and `docs/PROGRESS.md` for what's already done.

## Phase 1 — Project Scaffolding & Environment Setup

### Goal
A repo with a running FastAPI backend and a running React (Vite) frontend, both connected to a real Supabase project, ready for Phase 2 (schema).

### Tasks

- [ ] `git init` at the project root; root `.gitignore` (node_modules, venv/__pycache__, .env, build output).
- [ ] `backend/` — FastAPI app:
  - [ ] Python virtual environment
  - [ ] `requirements.txt`: fastapi, uvicorn, sqlalchemy, psycopg2-binary (or asyncpg), pydantic-settings, python-dotenv, python-multipart, passlib[bcrypt], python-jose, supabase (python client)
  - [ ] `app/main.py` — FastAPI instance, CORS middleware, `/health` route
  - [ ] `app/core/config.py` — settings loaded from env (Supabase URL/keys, DB URL, auth secret)
  - [ ] `.env.example` with the variable names (no real secrets committed)
  - [ ] Confirm `uvicorn app.main:app --reload` runs locally and `/health` responds
- [ ] `frontend/` — React (Vite) app:
  - [ ] Scaffold with `npm create vite@latest frontend -- --template react`
  - [ ] Install dependencies, confirm `npm run dev` runs
  - [ ] `.env.example` for `VITE_API_URL`
  - [ ] Basic router set up (public apply page route, admin login route, admin dashboard route) — placeholder pages for now
- [ ] Supabase project:
  - [ ] Create the project (or confirm one exists)
  - [ ] Record project URL + keys somewhere safe (not committed) — note in `docs/PROGRESS.md` that this step is done, without the secrets themselves
- [ ] Confirm backend can connect to the Supabase Postgres instance (a trivial query or connection check)

### Exit criteria
- Backend runs locally and responds on `/health`.
- Frontend runs locally and renders a placeholder page.
- Supabase project exists and the backend can reach its database.
- Nothing here touches schema, auth logic, or UI yet — that starts in Phase 2/3.
