# PRODUCT_VISION.md

How the product looks and feels. Written before any technical planning — see `docs/ROADMAP.md` for how it gets built.

Two separate front-ends, one shared backend:

- **Public Application Page** — anyone with the link can open it and apply.
- **Admin Dashboard** — the `admin@enter.in` login only. Manages jobs and moves candidates through the pipeline.

Both are plain, fast, and uncluttered. No dashboard widgets, no unnecessary steps, no heavy design system. A candidate should be able to apply in under a minute. An admin should be able to scan the candidate list and move someone a stage in one or two clicks.

## Public Application Page

One screen, one form. No login, no navigation, no distractions.

Layout, top to bottom:
1. A short heading — what the page is for (e.g. "Apply for a job at enter").
2. Job dropdown — lists open jobs by title (with department/location shown alongside if it helps tell them apart).
3. Form fields: Name, Phone, Email, Resume upload, Note (short textarea).
4. Submit button.
5. On success: the form is replaced by a simple confirmation message. No redirect, no account created, nothing else to do.

Validation errors show inline, next to the field, in plain language ("Enter a valid email").

Mobile-friendly by default — this link may be shared and opened on a phone.

## Admin Dashboard

### Login screen
- Just email + password, a submit button, and an error message on failure. Nothing else on this screen.

### Once logged in

Two areas, reachable without a page reload feel (client-side routing):

**Jobs**
- A table/list of jobs: title, department/location, created date, and an edit/delete action per row.
- An "Add job" action opens a small form (title, department/location, description) — inline or a modal, not a separate heavy page.
- Deleting a job asks for confirmation (it may have applications attached).

**Candidates**
- A table of every application: name, phone, email, job applied for, current stage, submitted date, and a link/button to open the resume.
- Two filters at the top: by job, by stage. Both can be combined. A "clear filters" option.
- Changing a candidate's stage happens right in the row — a dropdown or a small set of stage buttons, no separate edit screen. The change saves immediately.
- The stage list matches `docs/REQUIREMENTS.md`: Applied, Reject, R1, R1 Reject, R2, R2 Reject, R3, R3 Reject, Approved.

### Tone of the UI

Utilitarian, not flashy. Think a clean internal tool: readable tables, clear buttons, obvious states (loading, empty, error). A light color used for stage status is fine (e.g. green for Approved, red for the Reject stages) as long as it's still readable as plain text without relying on color alone.

No dark mode requirement, no animations beyond basic transitions, no onboarding flow. Get an admin looking at real candidate data as fast as possible after login.
