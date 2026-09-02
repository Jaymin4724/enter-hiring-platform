# PLAN.md

Detailed plan for the **current phase only**. Replaced entirely when this phase is done — see `docs/ROADMAP.md` for the full phase list, `docs/PROGRESS.md` for what's already done, and `docs/TEST.md` for the test checklist this phase must satisfy before it's marked complete.

## Phase 9 — Seed, QA & Submission Polish

### Goal
Final sanity pass before calling this submittable. Much of this phase's checklist was already verified organically while fixing deployment issues in Phase 8 (a real application was submitted and confirmed on the live site, then cleaned up) — this phase is about deliberately re-confirming everything is in the state it should be for a reviewer opening the links cold, not building anything new.

### Tasks

- [ ] Confirm production DB state: exactly 10 jobs, 1 admin, and the 10 demo candidates (from `seed_demo_candidates.py`) — no leftover test data from deployment debugging
- [ ] Full walkthrough on the **hosted** links only (not localhost), as a reviewer would experience it:
  - [ ] Open the public page cold, apply for a job with a real file, see the success screen
  - [ ] Open the admin dashboard, log in, see the new application appear
  - [ ] Move it through a couple of stages, confirm it sticks
  - [ ] Check the resume link works
  - [ ] Clean up whatever test data this walkthrough creates
- [ ] Check browser console on both hosted pages for any errors/warnings worth fixing
- [ ] Re-read `README.md` end to end as a first-time reviewer would — confirm it's accurate, the live links work, admin credentials are correct
- [ ] Final review of `docs/PROGRESS.md` — does it read as a coherent account of the whole build, decisions and all?

### Exit criteria
- All Phase 9 boxes in `docs/TEST.md` are checked.
- Someone with zero context could open `README.md`, click the two live links, and understand + use the product without asking a question.
- This is the last phase — after this, the project is done.
