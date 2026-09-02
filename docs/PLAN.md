# PLAN.md

Detailed plan for the **current phase only**. Replaced entirely when this phase is done — see `docs/ROADMAP.md` for the full phase list, `docs/PROGRESS.md` for what's already done, and `docs/TEST.md` for the test checklist this phase must satisfy before it's marked complete.

## Phase 6 — Frontend: Admin Dashboard (Login & Jobs)

### Goal
A working login screen and a jobs management UI, styled per the Linear-inspired admin direction agreed in Phase 5 (dense, one accent color, inline editing — reusing the design tokens already in `frontend/src/index.css`).

### Tasks

- [ ] `frontend/src/lib/auth.js` — store/read the JWT (localStorage is fine here — it's an internal tool, not the public page), `login(email, password)` calling `POST /auth/login`, `logout()`, `getToken()`
- [ ] Update `frontend/src/lib/api.js` — attach `Authorization: Bearer <token>` to admin-only calls; add `createJob`, `updateJob`, `deleteJob`
- [ ] Add shadcn components needed: `table`, `badge`, `dialog` (or `sheet` for the slide-over per `docs/PRODUCT_VISION.md`), `dropdown-menu`, `form` (or hand-rolled — match the pattern already used in `ApplyPage.jsx`)
- [ ] `pages/AdminLogin.jsx` — email + password form, calls `login()`, redirects to `/admin` on success, shows an inline error on 401
- [ ] A route guard (e.g. `components/RequireAuth.jsx`) wrapping `/admin` — redirects to `/admin/login` if no token
- [ ] `pages/AdminDashboard.jsx` — top nav (Jobs / Candidates tabs — Candidates tab is a Phase 7 stub for now), logout button
- [ ] Jobs view:
  - [ ] Table: title, department, location, created date, edit/delete actions per row
  - [ ] "Add job" opens a slide-over/dialog with title/department/location/description fields → `POST /jobs`
  - [ ] Edit reuses the same form, prefilled → `PUT /jobs/{id}`
  - [ ] Delete asks for confirmation, then `DELETE /jobs/{id}`
  - [ ] List refreshes after create/edit/delete (refetch or optimistic update)

### Manual test pass (check off in `docs/TEST.md` Phase 6 when done)
- [ ] Wrong credentials show an error on the login screen
- [ ] Correct credentials reach the dashboard
- [ ] Visiting `/admin` while logged out redirects to `/admin/login`
- [ ] Create/edit/delete a job from the UI is reflected immediately in the list

### Exit criteria
- An admin can log in, land on the dashboard, and fully manage jobs from the browser — no more curl/Swagger needed for job management.
- The 10 seeded jobs are still intact after this phase's manual testing (clean up any test jobs created during verification).
- No candidates UI yet — that's Phase 7.
