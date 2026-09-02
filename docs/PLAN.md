# PLAN.md

Detailed plan for the **current phase only**. Replaced entirely when this phase is done — see `docs/ROADMAP.md` for the full phase list and `docs/PROGRESS.md` for what's already done.

## Phase 2 — Supabase Schema & Storage Setup

### Goal
Real tables in the Supabase Postgres database, a resume storage bucket, and a seed script that populates 10 jobs and the one admin account — everything Phase 3/4 API work will read and write against.

### Tasks

- [ ] Define SQLAlchemy models in `backend/app/models/`:
  - [ ] `Job` — id, title, department, location, description, created_at
  - [ ] `Application` — id, job_id (FK), name, phone, email, resume_path, note, stage, created_at, updated_at
  - [ ] `Admin` — id, email, password_hash
- [ ] `backend/app/core/db.py` — SQLAlchemy engine + session, reading `DATABASE_URL` from settings
- [ ] Create the tables (Alembic migration, or a simple `create_all()` bootstrap script — pick whichever is faster; note the choice in `docs/PROGRESS.md`)
- [ ] Create a `resumes` bucket in Supabase Storage (private, not public — resumes shouldn't be world-readable by URL guessing)
- [ ] `backend/app/services/seed.py` — seed script:
  - [ ] Insert 10 sample jobs (varied titles/departments so the dropdown looks real)
  - [ ] Insert the admin account: email `admin@enter.in`, a chosen password (hashed with passlib/bcrypt) — record the plaintext password in `docs/PROGRESS.md` for submission, not in the repo
- [ ] Run the seed script against the real Supabase DB and confirm rows exist (quick `SELECT` check)

### Exit criteria
- `jobs`, `applications`, `admins` tables exist in Supabase with the right columns.
- 10 jobs and 1 admin row are present in the database.
- A `resumes` storage bucket exists.
- Nothing here builds API routes or UI yet — that's Phase 3 onward.
