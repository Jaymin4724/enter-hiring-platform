# PLAN.md

Detailed plan for the **current phase only**. Replaced entirely when this phase is done — see `docs/ROADMAP.md` for the full phase list and `docs/PROGRESS.md` for what's already done.

## Phase 3 — Backend API: Auth & Jobs

### Goal
Admin can log in over the API, and jobs are fully CRUD-able. Public read-only jobs endpoint exists for the candidate-facing dropdown.

### Tasks

- [ ] Pydantic schemas in `backend/app/schemas/`:
  - [ ] `job.py` — `JobCreate`, `JobUpdate`, `JobOut`
  - [ ] `auth.py` — `LoginRequest`, `TokenResponse`
- [ ] `app/services/auth.py`:
  - [ ] `verify_password` / password check using `bcrypt` directly (not passlib — see `docs/PROGRESS.md`)
  - [ ] JWT create/decode helpers (`python-jose`), using `settings.auth_secret_key` and `settings.auth_token_expire_minutes`
  - [ ] FastAPI dependency `get_current_admin` that reads the bearer token and loads the `Admin` row
- [ ] `app/api/auth.py` router:
  - [ ] `POST /auth/login` — email+password against `admins` table, returns a JWT on success, 401 on failure
- [ ] `app/api/jobs.py` router:
  - [ ] `GET /jobs` — public, list all jobs (for the candidate dropdown)
  - [ ] `POST /jobs` — admin-only, create
  - [ ] `PUT /jobs/{id}` — admin-only, update
  - [ ] `DELETE /jobs/{id}` — admin-only, delete (applications referencing it cascade per the model relationship)
- [ ] Wire both routers into `app/main.py`
- [ ] Manual check: login with `admin@enter.in` / the seeded password, use the token to create/edit/delete a job, confirm `GET /jobs` works without a token

### Exit criteria
- `/auth/login` issues a working token for the seeded admin and rejects bad credentials.
- Jobs CRUD works end-to-end against the real Supabase DB, protected by the token where required.
- `GET /jobs` works with no auth — the public form will call this in Phase 5.
- No application-submission or resume-upload logic yet — that's Phase 4.
