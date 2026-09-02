# REQUIREMENTS.md

## Project

**enter — AI Fullstack Intern Technical Assignment**
A candidate application and hiring management system.

Source: `AI Full Stack Developer Intern Assignment.pdf`

## Objective

Build a simple, working system with two parts:

1. A **public job application page** — candidates apply for a job.
2. An **admin dashboard** — an admin manages jobs and moves applications through hiring stages.

Priorities, in order: functionality, clean implementation, usability, speed. Not a visually heavy UI.

## Part 1 — Public Application Page

- Open link, no login needed. Anyone can open it and apply.
- Job is chosen from a dropdown.
  - Seed data: 10 sample jobs (title, and any other fields needed to show in the dropdown, e.g. department/location).
- Application form fields:
  - Name
  - Phone
  - Email
  - Resume upload (file)
  - Job (dropdown selection)
  - A brief note (free text)
- On submit, the application is saved and becomes visible in the admin dashboard, in the "Applied" stage.
- Basic validation: required fields, valid email format, valid phone format, resume file type/size limit.

## Part 2 — Admin Dashboard

### Login

- Simple email + password login. No signup flow.
- One seeded admin account:
  - Email: `admin@enter.in`
  - Password: to be set at seed time (not specified in the assignment — pick a value and document it in the submission).
- Only logged-in admins can reach the dashboard.

### Job management

Admin can:
- Create a job
- Edit a job
- Delete a job
- View the list of jobs

A job needs at least: title, and enough fields to display meaningfully in the candidate-facing dropdown (e.g. department, location, description). Jobs created here are the same jobs that appear in the Part 1 dropdown.

### Candidate / application management

- Admin sees all candidates who applied, across all jobs, with every field captured on the public form (name, phone, email, resume, job applied for, note, submission date).
- Admin can open/download the uploaded resume.
- Admin can filter the candidate list by job.
- Admin can filter the candidate list by stage.
- Admin can move an application between stages.

### Application stages

Fixed pipeline, in this order:

1. Applied (initial — set automatically on submission)
2. Reject
3. R1
4. R1 Reject
5. R2
6. R2 Reject
7. R3
8. R3 Reject
9. Approved

The admin manually moves an application to any of these stages; there's no requirement in the assignment that transitions be restricted to a strict forward-only order, so allow free movement between stages unless the user says otherwise.

## Non-functional requirements

- Must be hosted online (not just runnable locally).
- Submission must include two working links:
  - The public candidate application page.
  - The admin dashboard.
- Keep the UI simple and fast — no requirement for a polished design system.

## Data model (minimum)

**Job**
- id
- title
- department / location (or similar descriptive fields)
- description (optional but useful for the dropdown/context)
- created_at

**Application**
- id
- job_id (references Job)
- name
- phone
- email
- resume (file reference/URL)
- note
- stage (one of the 9 stages above; defaults to "Applied")
- created_at
- updated_at

**Admin**
- id
- email (seeded: admin@enter.in)
- password (hashed)

## Decisions made

- **Tech stack**: Python/FastAPI backend, React frontend, Supabase (Postgres + Storage) for data and resume files.
- **Hosting**: frontend on Vercel, backend on Render, database/storage on Supabase.
- **Admin password** — the assignment gives only the email; a password needs to be chosen and documented for the submission. See `docs/PROGRESS.md` for the seeded value once set.
- **Auth mechanism** — decided in Phase 1/3 planning (see `docs/PLAN.md` / `docs/ROADMAP.md`).
- **Resume storage** — Supabase Storage bucket.

See `docs/PRODUCT_VISION.md` for how the product looks and feels, and `docs/ROADMAP.md` for the phase-by-phase technical build plan.

## Deliverables

- Working hosted URL for the public application page.
- Working hosted URL for the admin dashboard.
- Seeded data: 10 jobs, 1 admin account.
- Source code.

## Timeline

24 hours from assignment receipt.
