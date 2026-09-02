# PLAN.md

Detailed plan for the **current phase only**. Replaced entirely when this phase is done — see `docs/ROADMAP.md` for the full phase list, `docs/PROGRESS.md` for what's already done, and `docs/TEST.md` for the test checklist this phase must satisfy before it's marked complete.

## Phase 5 — Frontend: Public Application Page

### Goal
`frontend/src/pages/ApplyPage.jsx` becomes a real, working form: loads jobs from the live API, lets a candidate submit an application with a resume, validates input, and shows a clear success state. This is the first frontend phase to actually talk to the backend built in Phases 3–4.

### Tasks

- [ ] `frontend/src/lib/api.js` — small fetch wrapper reading `VITE_API_URL`, with a `getJobs()` and `submitApplication(formData)` helper (the latter posts `multipart/form-data`, matching `POST /applications`)
- [ ] `ApplyPage.jsx`:
  - [ ] On mount, fetch `GET /jobs`, populate the dropdown (label: title — department/location)
  - [ ] Form fields: Name, Phone, Email, Resume (file input), Job (dropdown), Note (textarea)
  - [ ] Client-side validation before submit: required fields, basic email pattern, basic phone pattern, resume file present — mirrors the backend's own checks in `app/api/applications.py` so bad input is caught before a round trip
  - [ ] Submit → `POST /applications`; on success, replace the form with a confirmation message (per `docs/PRODUCT_VISION.md` — no redirect)
  - [ ] Surface backend validation errors (422/404 responses) inline, in plain language, not raw JSON
  - [ ] Loading state on submit (disable the button, avoid double-submit)
- [ ] Basic responsive styling — mobile-friendly per `docs/PRODUCT_VISION.md` (this link may be opened on a phone)
- [ ] `frontend/.env` created locally from `.env.example` with `VITE_API_URL` pointing at the local backend (`http://localhost:8000`)

### Manual test pass (see `docs/TEST.md` Phase 5 — check these off there when done)
- [ ] Job dropdown loads real jobs from the API
- [ ] Submitting a valid application shows the success state
- [ ] Missing/invalid field shows an inline validation error, not a silent failure
- [ ] Resume upload works end to end — confirm the file lands in Supabase Storage (e.g. via the `GET /applications/{id}/resume` endpoint or the Supabase dashboard) after a real submission

### Exit criteria
- A real application, submitted through the browser UI, appears in the database with stage `"Applied"` and a working resume file.
- All four manual checks above pass.
- No admin-side UI yet — that's Phase 6.
