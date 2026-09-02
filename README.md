# enter — Hiring Platform

A candidate application + hiring management system, built for the **enter AI Fullstack Intern technical assignment**. Two surfaces, one backend:

- **Public application page** — anyone can apply to an open job, no login.
- **Admin dashboard** — a single admin account manages jobs and moves candidates through a 9-stage hiring pipeline.

## Live links

- **Public application page**: https://enter-hiring-platform.vercel.app/
- **Admin dashboard**: https://enter-hiring-platform.vercel.app/admin/login
- **Backend API**: https://enter-hiring-platform.onrender.com

Verified working end to end on these live links: applied for a real job on the hosted public page, confirmed it appeared in the hosted admin dashboard with the correct job, stage, and a working resume link — then cleaned up that test data.

**Note on cold starts**: the backend is on Render's free tier, which spins down after 15 minutes of no traffic and takes 30-60s to wake up on the next request. If the site feels slow to load jobs on first visit, that's why — not a bug.

## Quick start (local)

**Backend**
```
cd backend
python -m venv venv
./venv/Scripts/pip install -r requirements.txt
cp .env.example .env        # fill in Supabase URL/keys + DATABASE_URL
./venv/Scripts/python -m uvicorn app.main:app --reload   # http://localhost:8000/docs
```

**Frontend**
```
cd frontend
npm install
cp .env.example .env        # VITE_API_URL, defaults to http://localhost:8000
npm run dev                 # http://localhost:5173
```

**Admin login** (for review): `admin@enter.in` / `Enter@Hiring2026`

**Demo data**: 10 jobs and 10 realistic fake candidate applications (each with a real generated resume PDF, spread across different pipeline stages) come seeded — see `backend/seed.py` and `backend/seed_demo_candidates.py` if you want to regenerate them.

## Tech stack, and why

| Layer | Choice | Why |
|---|---|---|
| Backend | Python, FastAPI | Fast to build, automatic OpenAPI docs (`/docs`), good async/validation story via Pydantic. |
| Frontend | React + Vite | Standard, fast dev loop. |
| Styling | Tailwind CSS v4 + shadcn/ui | Accessible components out of the box (Radix under the hood) instead of hand-rolling dialogs/dropdowns/tables under a 24h clock. |
| Database + file storage | Supabase (Postgres + Storage) | One provider for both the relational data and resume files, generous free tier, fast to stand up. |
| Auth | Custom JWT (PyJWT) + bcrypt | The assignment only needed one hardcoded admin account — a full auth provider would be overkill. Chose PyJWT over the older `python-jose` after checking current guidance (FastAPI's own docs moved off it for maintenance reasons). |
| Hosting | Vercel (frontend) + Render (backend) | Free tier, minimal config, matches a small two-service app. |

## Architecture

```
Candidate ──▶ Public form (React) ──┐
                                     ├──▶ FastAPI backend ──▶ Supabase Postgres (jobs, applications, admin)
Admin ──▶ Login + Dashboard (React)─┘                    └──▶ Supabase Storage (resume files, private bucket)
```

One React app serves both surfaces (routed, not two separate deployables); one FastAPI backend serves both public and admin-only (JWT-gated) endpoints. Full endpoint list is browsable at `/docs` once the backend is running.

## Key decisions worth knowing about

- **One unified color system**, not separate palettes for the public page and admin dashboard — simpler to build and matches the assignment's own "don't over-engineer the UI" brief.
- **No database migration tool (Alembic)** — schema is created once via `Base.metadata.create_all()`. Not worth the tooling overhead for a single-shot schema on a short build; would revisit if the schema needed to evolve after real data existed.
- **Validation was hardened past the obvious happy path** — e.g. an all-whitespace name or an oversized field used to either slip through or crash the request with a raw 500. Found on review, fixed server-side (the source of truth) and mirrored client-side for fast feedback. Full rule-by-rule checklist, client and admin side, in [`docs/TEST.md`](docs/TEST.md#validation-checklist-client--admin).
- **Resumes are private**, not public files — access always goes through the backend, which hands out short-lived signed URLs to logged-in admins only, never a public link.
- **Demo/seed data** exists specifically so this doesn't look empty on first open — 10 realistic candidates with real generated resume content, spread across different pipeline stages, not just sitting in "Applied".

## What's implemented right now

- ✅ Public application form — job dropdown, all required fields, resume upload, full client+server validation, real success state.
- ✅ Admin login, protected routing.
- ✅ Admin jobs management — full create/edit/delete, mobile-friendly table.
- ✅ Admin candidates view — every field, job + stage filters (individually and combined), inline stage changes across all 9 pipeline stages, resume access via signed URLs.
- ✅ Backend — every endpoint the assignment asks for, JWT-protected where it should be, 36 automated tests passing.
- ✅ Hosting/deployment — frontend on Vercel, backend on Render, verified end to end on the live links above.

## Testing

Backend: `pytest` + FastAPI's `TestClient`, run against the real Supabase dev database (no mocking). 36 tests covering auth, jobs CRUD, and applications (submission, validation, filtering, stage transitions).
```
cd backend
./venv/Scripts/pip install -r requirements-dev.txt
./venv/Scripts/python -m pytest -v
```
Frontend has no automated suite (not worth it at this scope) — verified manually in the browser per the checklist in `docs/TEST.md`.

## Project documentation

This repo tracks its own planning process in `docs/`, in order:

| File | What's in it |
|---|---|
| [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md) | The assignment brief, translated into concrete requirements. |
| [`docs/PRODUCT_VISION.md`](docs/PRODUCT_VISION.md) | What the two surfaces should look and feel like. |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | The full build-phase breakdown and stack/hosting decision. |
| [`docs/PLAN.md`](docs/PLAN.md) | Detailed plan for whatever phase is currently in progress (replaced each phase). |
| [`docs/PROGRESS.md`](docs/PROGRESS.md) | The durable log — every decision made and what shipped in each phase, with reasoning. |
| [`docs/TEST.md`](docs/TEST.md) | Phase-by-phase test checklist, plus a consolidated client+admin validation checklist. |
| [`CLAUDE.md`](CLAUDE.md) | Codebase orientation for AI-assisted development on this repo. |
