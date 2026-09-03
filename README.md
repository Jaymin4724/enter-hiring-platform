# enter — Hiring Platform

A candidate application and hiring management system, built for the **enter AI Fullstack Intern technical assignment**. Two surfaces, one backend:

- **Public application page** — anyone can apply to an open job, no login required.
- **Admin dashboard** — a single admin account manages jobs and moves candidates through a 9-stage hiring pipeline.

## Live links

| | |
|---|---|
| Public application page | https://enter-hiring-platform.vercel.app/ |
| Admin dashboard | https://enter-hiring-platform.vercel.app/admin/login |
| Admin login | `admin@enter.in` / `Enter@Hiring2026` |
| Backend API docs | https://enter-hiring-platform.onrender.com/docs |

Verified end to end on these exact links: submitted a real application on the public page, confirmed it appeared correctly in the admin dashboard (right job, right stage, working resume), moved it through a pipeline stage, and confirmed the change persisted.

**Cold starts**: the backend runs on Render's free tier, which spins down after 15 minutes of no traffic and takes 30-60 seconds to wake on the next request. If the first load feels slow, that's why.

## Assignment requirements — status

| Requirement | Status |
|---|---|
| Public link, no login, apply to any job from a dropdown | ✅ |
| 10 seeded jobs | ✅ |
| Form: name, phone, email, resume upload, job, note | ✅ |
| Validation: required fields, email format, phone format, resume type/size | ✅ (server-side + mirrored client-side) |
| New applications land in "Applied" | ✅ |
| Admin login (email + password, no signup) | ✅ |
| Admin: create / edit / delete jobs | ✅ |
| Admin: view every candidate, every field captured | ✅ |
| Admin: open/download resume | ✅ (signed URL, private storage) |
| Admin: filter candidates by job | ✅ |
| Admin: filter candidates by stage | ✅ |
| Admin: move a candidate between stages | ✅ |
| All 9 stages (Applied → R1/R2/R3 + Reject variants → Approved) | ✅ |
| Hosted online, two working links | ✅ |

Full rule-by-rule breakdown (client-side and server-side, together) is in [`docs/TEST.md`](docs/TEST.md#validation-checklist-client--admin).

## Tech stack, and why

| Layer | Choice | Why |
|---|---|---|
| Backend | Python, FastAPI | Fast to build, automatic interactive API docs, strong request validation via Pydantic. |
| Frontend | React + Vite | Standard, fast dev loop. |
| Styling | Tailwind CSS v4 + shadcn/ui | Accessible components (Radix underneath) instead of hand-rolling dialogs, dropdowns, and tables from scratch under a tight timeline. |
| Database + file storage | Supabase (Postgres + Storage) | One provider for both relational data and resume files; fast to stand up. |
| Auth | Custom JWT (PyJWT) + bcrypt | The assignment needed exactly one hardcoded admin account — a full auth provider would be overkill. PyJWT chosen over the older `python-jose`, which FastAPI's own docs have moved away from for maintenance reasons. |
| Hosting | Vercel (frontend) + Render (backend) | Free tier, minimal configuration, matches a small two-service app. |

## Architecture

```
Candidate ──▶ Public form (React) ──┐
                                     ├──▶ FastAPI backend ──▶ Supabase Postgres (jobs, applications, admin)
Admin ──▶ Login + Dashboard (React)─┘                    └──▶ Supabase Storage (resume files, private bucket)
```

One React app serves both surfaces (routed, not two separate deployables); one FastAPI backend serves both the public and admin-only (JWT-gated) endpoints. Full endpoint list is browsable at `/docs`.

## Key decisions

- **One unified color system**, not separate palettes for the public page and admin dashboard — simpler to build and matches the assignment's own instruction not to over-engineer the UI.
- **No database migration tool.** Schema is created once via `Base.metadata.create_all()`. Not worth the tooling overhead for a fixed schema built in a single pass; would introduce one if the schema needed to evolve after real data existed.
- **Validation goes past the happy path.** Blank/whitespace-only fields and oversized input are rejected with a clear error, both server-side (the source of truth) and mirrored client-side for instant feedback. Full checklist in [`docs/TEST.md`](docs/TEST.md#validation-checklist-client--admin).
- **Resumes are private, not public files.** Access always goes through the backend, which issues short-lived signed URLs to logged-in admins only.
- **Realistic seed data.** 10 jobs and 10 fictional candidates (each with a generated, readable resume PDF) ship pre-loaded and spread across different pipeline stages, so the admin dashboard demonstrates a real, in-progress hiring pipeline rather than an empty table.

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

Demo data (10 jobs + 10 candidates with generated resumes) seeds via `backend/seed.py` and `backend/seed_demo_candidates.py`.

## Testing

Backend: `pytest` + FastAPI's `TestClient`, run against a real Postgres database (no mocking). 36 tests covering auth, jobs CRUD, and applications (submission, validation, filtering, stage transitions).
```
cd backend
./venv/Scripts/pip install -r requirements-dev.txt
./venv/Scripts/python -m pytest -v
```
Frontend has no automated suite — verified manually per the checklist in `docs/TEST.md`.

## Project documentation

This repo tracks its own planning process in `docs/`, in order:

| File | What's in it |
|---|---|
| [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md) | The assignment brief, translated into concrete requirements. |
| [`docs/PRODUCT_VISION.md`](docs/PRODUCT_VISION.md) | What the two surfaces should look and feel like. |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | The full build-phase breakdown and stack/hosting decision. |
| [`docs/PLAN.md`](docs/PLAN.md) | Detailed plan for whatever phase is currently in progress (empty once the project is complete). |
| [`docs/PROGRESS.md`](docs/PROGRESS.md) | The durable log — decisions made and what shipped in each phase, with reasoning. |
| [`docs/TEST.md`](docs/TEST.md) | Phase-by-phase test checklist, plus a consolidated client + admin validation checklist. |
| [`CLAUDE.md`](CLAUDE.md) | Codebase orientation for AI-assisted development on this repo. |
