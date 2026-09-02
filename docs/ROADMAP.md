# ROADMAP.md

Overall technical build plan. This is the full list of phases for the project — each phase gets its detailed, task-by-task breakdown in `docs/PLAN.md` only while it's the active phase. Once a phase is done, its detail in `PLAN.md` is replaced by the next phase's plan, and a short summary of what was done moves to `docs/PROGRESS.md`.

## Stack

- **Backend**: Python, FastAPI
- **Frontend**: React (Vite)
- **Database + file storage**: Supabase (Postgres + Storage)
- **Hosting**: frontend on Vercel, backend on Render, data on Supabase

## Phases

1. **Project Scaffolding & Environment Setup**
   Repo structure, FastAPI skeleton, React (Vite) skeleton, env config, Supabase project connected, local dev running for both.

2. **Supabase Schema & Storage Setup**
   `jobs`, `applications`, `admins` tables. Resume storage bucket. Seed script for 10 jobs + 1 admin.

3. **Backend API — Auth & Jobs**
   Admin login (email+password → session/token). Jobs CRUD endpoints, public read-only jobs list endpoint for the dropdown.

4. **Backend API — Applications**
   Public submit-application endpoint (with resume upload to Supabase Storage). Admin list/filter endpoint (by job, by stage). Stage-update endpoint.

5. **Frontend — Public Application Page**
   Job dropdown wired to the API, application form, validation, submit, success state.

6. **Frontend — Admin Dashboard: Login & Jobs**
   Login screen wired to auth. Protected routing. Jobs list, create/edit/delete.

7. **Frontend — Admin Dashboard: Candidates**
   Candidates table, job/stage filters, resume link, inline stage change.

8. **Deployment**
   Backend to Render, frontend to Vercel, environment variables wired on both, CORS configured, Supabase in production mode. Confirm both hosted links work end-to-end.

9. **Seed Data, QA & Submission Polish**
   Final seed of 10 jobs, walk both flows end-to-end, fix rough edges, write submission notes (links, admin credentials).

## Status

Current phase: see `docs/PLAN.md`.
Completed phases and key decisions: see `docs/PROGRESS.md`.
