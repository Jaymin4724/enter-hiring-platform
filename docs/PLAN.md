# PLAN.md

Detailed plan for the **current phase only**. Replaced entirely when this phase is done — see `docs/ROADMAP.md` for the full phase list, `docs/PROGRESS.md` for what's already done, and `docs/TEST.md` for the test checklist this phase must satisfy before it's marked complete.

## Phase 8 — Deployment

### Goal
Two real, working, hosted links: the public application page and the admin dashboard, both reachable from anywhere — the assignment's explicit deliverable.

### Tasks

- [ ] User creates a Render account, connects GitHub, grants access to this repo
- [ ] User creates a Vercel account, connects GitHub, grants access to this repo
- [ ] Deploy backend to Render (blueprint already prepared at `render.yaml`):
  - [ ] New > Blueprint, point at the repo, Render reads `render.yaml`
  - [ ] Fill in the `sync: false` env vars in the dashboard: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL`, `AUTH_SECRET_KEY` (copy from local `backend/.env`), and `FRONTEND_ORIGIN` (temporarily `http://localhost:5173`, fixed once the Vercel URL exists — see below)
  - [ ] Confirm the deployed backend responds: `https://<render-url>/health`
- [ ] Deploy frontend to Vercel:
  - [ ] New Project, import the repo, set **Root Directory** to `frontend`
  - [ ] Set env var `VITE_API_URL` to the real Render backend URL from the previous step
  - [ ] Deploy, confirm the site loads
- [ ] Go back to Render, update `FRONTEND_ORIGIN` to the real Vercel URL, let it redeploy
- [ ] End-to-end check on the **hosted** links (not localhost): submit a real application on the hosted public page, confirm it appears in the hosted admin dashboard
- [ ] Update `README.md`'s "Live links" section with the two real URLs

### Exit criteria
- All Phase 8 boxes in `docs/TEST.md` are checked.
- Both hosted URLs work end-to-end, CORS is correctly scoped to the real frontend origin (not left open or stuck on localhost).
- `README.md` has real, working links — ready for submission.
