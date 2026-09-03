# PROGRESS.md

Running summary of decisions made and phases completed. Detailed per-phase plans live in `docs/PLAN.md` (current phase only) — this file is the durable record after each phase's detail is truncated.

## Decisions

- 2026-09-02 — Stack chosen: Python/FastAPI backend, React (Vite) frontend, Supabase (Postgres + Storage) for data and resumes.
- 2026-09-02 — Hosting chosen: frontend on Vercel, backend on Render, Supabase for DB/storage.
- 2026-09-02 — Doc structure set: `REQUIREMENTS.md` → `PRODUCT_VISION.md` → `ROADMAP.md` → `PLAN.md` (current phase, replaced each phase) → `PROGRESS.md` (this file). All docs live in `docs/`, except `CLAUDE.md` which stays at repo root.
- 2026-09-02 — GitHub repo created: [Jaymin4724/enter-hiring-platform](https://github.com/Jaymin4724/enter-hiring-platform).

## Phases completed

### Phase 1 — Project Scaffolding & Environment Setup

- Git repo initialized. `backend/` scaffolded as a FastAPI app (venv, dependencies, `app/main.py` with CORS + `/health`, `app/core/config.py` for env-based settings). `frontend/` scaffolded via Vite (React + `react-router-dom`), placeholder routes wired for `/`, `/admin/login`, `/admin`.
- `.env.example` added for both; `.gitignore` covers `venv/`, `node_modules/`, and all `.env` files.
- Supabase project connected: `backend/.env` filled in with the project URL, keys, and `DATABASE_URL`. Direct Postgres connection verified working. `AUTH_SECRET_KEY` set to a generated random secret.

**Phase 1 is complete.**

### Phase 2 — Supabase Schema & Storage Setup

- SQLAlchemy models added: `Job`, `Application` (plus the 9-stage `STAGES` list), `Admin` — UUID primary keys.
- Tables created via `Base.metadata.create_all()` (a one-off `backend/create_tables.py` script) rather than a migration tool — not worth the tooling overhead for a schema built in a single pass; would introduce one if the schema needed to evolve after real data existed.
- Private `resumes` bucket created in Supabase Storage.
- Seed script (`backend/seed.py`) run against the real database: 10 jobs, 1 admin.
- **Admin login for review**: `admin@enter.in` / `Enter@Hiring2026`.
- Password hashing implemented with `bcrypt` directly rather than the `passlib` wrapper — `passlib`'s bcrypt backend detection doesn't work with current `bcrypt` releases, a known compatibility gap in that library.

**Phase 2 is complete.**

### Phase 3 — Backend API: Auth & Jobs

- Schemas added for jobs and auth (`JobCreate`/`JobUpdate`/`JobOut`, `LoginRequest`/`TokenResponse`).
- `services/auth.py`: password check via `bcrypt`, JWT create/decode, an `get_current_admin` dependency guarding admin-only routes.
- JWT handling uses **PyJWT** rather than `python-jose` — checked current guidance and found FastAPI's own documentation has moved off `python-jose` for maintenance reasons; PyJWT is the actively maintained choice.
- Routers added: `POST /auth/login`, and full `GET`/`POST`/`PUT`/`DELETE` on `/jobs` (public read, admin-only write).
- Automated test suite introduced (`pytest` + FastAPI's `TestClient`, run against the real database). 9 tests: login success/failure paths, public job listing, auth-gating on writes, and a full create→update→delete lifecycle.

**Phase 3 is complete.**

### Phase 4 — Backend API: Applications

- Schemas and storage service extended: resume upload validates content type (PDF/DOC/DOCX) and size (5MB cap) before landing in the private bucket.
- `POST /applications` (public, multipart — validates email, phone, resume type/size, and that the target job exists), `GET /applications` (admin-only, filterable by job and stage), `PATCH /applications/{id}/stage`, `GET /applications/{id}/resume` (signed URL).
- Test suite extended to 22 tests: every validation failure path, auth-gating, job/stage filtering, and all 9 stage values individually confirmed valid.

**Phase 4 is complete.**

### Phase 5 — Frontend: Public Application Page

- Product direction set for both surfaces: the candidate form modeled on clean, modern applicant-tracking UX (single-column card, drag-and-drop resume upload, inline validation); the admin dashboard modeled on a dense, functional internal tool (data table, colored status pills, inline editing).
- Design system: Tailwind CSS v4 + shadcn/ui, with one unified color palette shared across both surfaces rather than two separate ones — simpler to build and consistent with the assignment's preference for a light, unfussy UI. Custom `--color-stage-*` tokens map the 9 hiring stages to a clear color progression (neutral → blue → indigo → violet → green, red for every reject variant).
- `ApplyPage.jsx` built as a fully working page: job dropdown loaded from the API, all required fields, a custom drag-and-drop resume component (no off-the-shelf primitive covers this), client-side validation mirroring the backend's rules, and a real success state.
- Verified live in the browser: all 10 jobs load, empty-submit shows every inline validation error with no network call, and a full valid submission (real uploaded file) was cross-checked against the database — correct job, stage `Applied`, resume path set.

**Phase 5 is complete.**

### Validation hardening (cross-cutting fix to Phase 4's `POST /applications`)

- Found two real gaps on review: a whitespace-only name was silently accepted (FastAPI's required-field check only requires the key be present, not non-blank), and there was no upper length limit on `name`/`note` — an oversized value would hit the database directly and surface as an unhandled 500 instead of a clean validation error.
- Fixed server-side (strip and validate before storage, explicit length caps) and mirrored client-side (matching checks plus `maxLength` on the inputs). Four new test cases added; suite now 26 tests.

### Phase 6 — Frontend: Admin Dashboard (Login & Jobs)

- Token-based auth on the frontend: `lib/auth.js` stores the JWT, `lib/api.js` attaches it automatically to admin requests, `RequireAuth.jsx` guards the `/admin` routes and redirects to login when signed out.
- `AdminLogin.jsx` (real login form, inline error on failure) and `AdminDashboard.jsx` (the layout shell — top nav, logout — wrapping nested `/admin/jobs` and `/admin/candidates` routes).
- `JobsPage.jsx`: full jobs CRUD — a table, a slide-over form for create/edit, a confirmation dialog for delete.
- Mobile-friendliness treated as a hard requirement, not an afterthought: tables scroll horizontally on narrow screens instead of breaking layout, and icon-only action buttons are sized for comfortable tapping (40px, larger than the component library's default).
- Verified live in the browser: full login → jobs CRUD → logout cycle, and the route guard redirecting correctly in both directions.
- The same validation gap found in Phase 4 turned up in the jobs API too — a blank job title was accepted, with no length caps. Fixed the same way: server-side validation as the source of truth (restructured so it can never affect reading existing data), with 9 new test cases covering both create and update. Suite now 36 tests.
- Realistic demo data added: a script generates 10 one-page resume PDFs for fictional candidates and submits them through the real API, spread across the hiring pipeline — so the admin dashboard demonstrates a genuine in-progress pipeline rather than an empty table.

**Phase 6 is complete.**

### Phase 7 — Frontend: Admin Dashboard (Candidates)

- `CandidatesPage.jsx` built out: job and stage filters (individually and combined), a table showing every field captured on the public form, and a notable design economy — the per-row stage control **is** the colored status pill (one styled dropdown, not a separate badge next to a plain select). Resume links are fetched on click, not prefetched for every row.
- Small navigation conveniences added for usability: an "Admin login" link from the public page, and "Home"/"Back to Home" links on the admin side.
- Verified live in the browser against the seeded demo candidates: filters narrow the list correctly, a real stage change persisted after a page reload, and a resume link opened a genuine, working file.
- Deployment prep: added a Render Blueprint (`render.yaml`) defining the backend service, with secrets configured to be entered directly in Render's dashboard rather than ever committed.

**Phase 7 is complete.**

### Phase 8 — Deployment

Backend deployed to Render, frontend to Vercel. Several real, environment-specific issues surfaced during rollout and were root-caused individually:

- **Render's default plan is paid.** The blueprint's web service needed `plan: free` set explicitly — omitting it defaults to a paid compute tier.
- **Start command.** Render's own auto-detected default (a generic guess unrelated to this project) needed to be overridden with the actual one: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- **Database connectivity in production.** Supabase's direct Postgres connection resolves IPv6-only, and Render (like most free-tier PaaS platforms) has no outbound IPv6 — so the backend could reach the database locally but not once deployed. Fixed by switching `DATABASE_URL` in production to Supabase's Session Pooler connection string, which is IPv4-compatible. Local development is unaffected.
- **CORS configuration.** The backend's CORS middleware is built around a single allowed origin, by design; the fix was making sure exactly one — the real production frontend URL — was configured.
- **Client-side routing on Vercel.** Direct navigation to a route like `/admin/login` returned Vercel's own 404 instead of reaching the React app, because a static host doesn't know to serve `index.html` for client-side routes unless told to. Fixed with a `vercel.json` rewrite rule.
- Full end-to-end verification on the live, hosted links: a real application was submitted on the public page and confirmed to appear correctly in the admin dashboard, then the test data was cleaned up.

**Phase 8 is complete.**

### Phase 9 — Seed, QA & Submission Polish

- Confirmed production data was clean before final QA: exactly 10 jobs, 10 demo candidates, no leftover test data from deployment debugging.
- Full cold-reviewer walkthrough on the live hosted links: submitted a real application with an uploaded resume, confirmed zero console errors, confirmed the application appeared correctly via the admin API, moved it through a pipeline stage and confirmed the change persisted, confirmed the resume link resolves to a real file — then cleaned up.
- `README.md` reviewed end to end as a first-time reviewer would read it, and corrected a stale line left over from before deployment shipped.

**Phase 9 is complete. This was the last phase — the project is done.**
