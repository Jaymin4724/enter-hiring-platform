# PLAN.md

Detailed plan for the **current phase only**. Replaced entirely when this phase is done — see `docs/ROADMAP.md` for the full phase list, `docs/PROGRESS.md` for what's already done, and `docs/TEST.md` for the test checklist this phase must satisfy before it's marked complete.

## Phase 7 — Frontend: Admin Dashboard (Candidates)

### Goal
The admin can see every candidate who applied, across all jobs, with every field captured on the public form — filter by job and stage, open the resume, and move someone through the pipeline right from the table. This is the last piece before deployment; the 10 real demo candidates seeded in Phase 6 (`backend/seed_demo_candidates.py`) make this phase demoable with realistic data from the start.

### Tasks

- [ ] `frontend/src/lib/api.js` — add `getApplications({ jobId, stage })` (query params), `updateApplicationStage(id, stage)`, `getResumeUrl(id)`
- [ ] `frontend/src/pages/admin/CandidatesPage.jsx` — replace the stub with the real view:
  - [ ] Table: Name, Email, Phone, Job title, Stage (as a colored `Badge` using the existing `--color-stage-*` tokens from `frontend/src/index.css` — reuse them, don't invent new colors), Applied date, Resume link
  - [ ] Job filter + Stage filter (shadcn `Select`s) above the table, both optional and combinable — re-fetch (or client-filter, if the candidate list is small enough that it's simpler) when either changes
  - [ ] Stage change inline in the row — a `Select` per row calling `updateApplicationStage`, no separate edit screen, per `docs/PRODUCT_VISION.md`
  - [ ] Resume link opens the signed URL from `getResumeUrl` in a new tab
  - [ ] Loading/empty/error states, mobile-friendly table (same `overflow-x-auto` pattern already proven in `JobsPage.jsx`)
- [ ] Verify in the browser: filters work individually and combined, a stage change persists after reload, resume link actually opens the PDF

### Manual test pass (check off in `docs/TEST.md` Phase 7 when done)
- [ ] Candidates table shows every field captured on the public form
- [ ] Job filter and stage filter work individually and combined
- [ ] Changing a candidate's stage in the row persists after a page reload
- [ ] Resume link/download works from the row

### Exit criteria
- All Phase 7 boxes in `docs/TEST.md` are checked.
- The full candidate-facing and admin-facing product now works end to end locally — deployment (Phase 8) is the only thing left before submission.
