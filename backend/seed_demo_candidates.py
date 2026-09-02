"""One-off bootstrap: seed 10 realistic demo candidates (with generated resume PDFs)
applying to the 10 already-seeded jobs, spread across the hiring pipeline stages.

Submits through the real public API (POST /applications) so it exercises the same
validation/storage path a real candidate would, then moves each application's stage
via the admin API. Safe to re-run — skips any candidate whose email already applied.

Run with: ./venv/Scripts/python.exe seed_demo_candidates.py
(requires the backend running locally on http://localhost:8000)
"""

import os

import requests
from fpdf import FPDF
from fpdf.enums import XPos, YPos

API_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@enter.in"
ADMIN_PASSWORD = "Enter@Hiring2026"

RESUME_DIR = os.path.join(os.path.dirname(__file__), "seed_data", "resumes")

# One candidate per already-seeded job (backend/seed.py), matched by job title.
CANDIDATES = [
    {
        "first_name": "Aarav",
        "last_name": "Sharma",
        "job_title": "Backend Engineer",
        "phone": "+91 98765 43210",
        "note": "Excited about the backend role — I've been building REST APIs in Python for 3 years.",
        "summary": "Backend engineer with 3+ years building REST APIs and data-heavy services in Python.",
        "bullets": [
            "Built and maintained FastAPI/Django services handling 2M+ requests/day.",
            "Designed Postgres schemas and optimized slow queries, cutting p95 latency by 40%.",
            "Set up CI pipelines and integration test suites for two backend teams.",
        ],
        "education": "B.Tech in Computer Science, VIT Vellore",
        "skills": "Python, FastAPI, Django, PostgreSQL, Redis, Docker, REST APIs",
        "stage": "Applied",
    },
    {
        "first_name": "Diya",
        "last_name": "Patel",
        "job_title": "Frontend Engineer",
        "phone": "+91 91234 56789",
        "note": "Frontend developer who loves clean, accessible UI — would love to work on the candidate app.",
        "summary": "Frontend engineer focused on React, accessible UI, and fast, maintainable component libraries.",
        "bullets": [
            "Led a migration from class components to React hooks across a 40k-LOC codebase.",
            "Built a shared component library adopted by 5 product teams.",
            "Improved Lighthouse performance scores from 62 to 94 on the main product.",
        ],
        "education": "B.E. in Information Technology, Pune Institute of Computer Technology",
        "skills": "React, TypeScript, Tailwind CSS, Vite, Accessibility (WCAG), Jest",
        "stage": "R1",
    },
    {
        "first_name": "Vihaan",
        "last_name": "Reddy",
        "job_title": "DevOps Engineer",
        "phone": "+91 90123 45678",
        "note": "DevOps engineer with hands-on experience running production infra on AWS.",
        "summary": "DevOps engineer specializing in CI/CD, containerized deployments, and cloud infrastructure on AWS.",
        "bullets": [
            "Migrated a monolith to containerized microservices on ECS, cutting deploy time by 70%.",
            "Built Terraform modules to standardize infra across 3 environments.",
            "Ran on-call rotation for a 99.95% uptime production system.",
        ],
        "education": "B.Tech in Electronics & Communication, IIIT Hyderabad",
        "skills": "AWS, Terraform, Docker, Kubernetes, GitHub Actions, Linux",
        "stage": "R1",
    },
    {
        "first_name": "Ananya",
        "last_name": "Iyer",
        "job_title": "QA Engineer",
        "phone": "+91 99887 76655",
        "note": "QA engineer passionate about catching issues before customers do.",
        "summary": "QA engineer with a mix of manual and automated testing experience across web and API products.",
        "bullets": [
            "Built an end-to-end Playwright test suite covering 80% of critical user flows.",
            "Reduced regression-testing cycle time from 3 days to 4 hours via automation.",
            "Partnered with engineering to set up a bug triage process that cut reopen rate by half.",
        ],
        "education": "B.Sc in Computer Science, Fergusson College, Pune",
        "skills": "Playwright, Selenium, Postman, pytest, Test Planning, JIRA",
        "stage": "R2",
    },
    {
        "first_name": "Kabir",
        "last_name": "Nair",
        "job_title": "Product Manager",
        "phone": "+91 97654 32109",
        "note": "PM background in B2B SaaS — interested in owning the hiring platform roadmap.",
        "summary": "Product manager with 4 years shipping B2B SaaS features end-to-end, from discovery to launch.",
        "bullets": [
            "Owned the roadmap for an onboarding product used by 500+ business customers.",
            "Ran user research and cut new-user time-to-value by 35% via a redesigned setup flow.",
            "Partnered with design and engineering leads to ship a major feature every 6 weeks.",
        ],
        "education": "MBA, Indian Institute of Management, Bangalore",
        "skills": "Product Strategy, User Research, Roadmapping, SQL, A/B Testing",
        "stage": "R2",
    },
    {
        "first_name": "Ishita",
        "last_name": "Verma",
        "job_title": "UI/UX Designer",
        "phone": "+91 96543 21098",
        "note": "Product designer who cares about fast, simple flows — big fan of the assignment brief's approach.",
        "summary": "Product designer focused on simple, fast, usable flows for both consumer and internal tools.",
        "bullets": [
            "Redesigned a multi-step signup flow, raising completion rate from 58% to 81%.",
            "Built and maintained a design system used across 4 product surfaces.",
            "Ran usability testing sessions that directly shaped 3 shipped features.",
        ],
        "education": "B.Des in Communication Design, NID Ahmedabad",
        "skills": "Figma, Design Systems, Prototyping, Usability Testing, Interaction Design",
        "stage": "R3",
    },
    {
        "first_name": "Rohan",
        "last_name": "Gupta",
        "job_title": "Data Analyst",
        "phone": "+91 95432 10987",
        "note": "Data analyst excited to build out hiring funnel metrics and reporting.",
        "summary": "Data analyst experienced in building dashboards and funnel analysis for product and growth teams.",
        "bullets": [
            "Built a self-serve analytics dashboard used weekly by 6 teams.",
            "Ran a funnel analysis that identified a drop-off point, informing a fix that lifted conversion 12%.",
            "Automated a manual weekly reporting process, saving ~5 hours/week.",
        ],
        "education": "B.Sc in Statistics, St. Xavier's College, Mumbai",
        "skills": "SQL, Python (pandas), Tableau, Looker, A/B Testing",
        "stage": "Approved",
    },
    {
        "first_name": "Meera",
        "last_name": "Joshi",
        "job_title": "Talent Acquisition Specialist",
        "phone": "+91 94321 09876",
        "note": "TA specialist with 3 years running full-cycle recruiting for tech roles.",
        "summary": "Talent acquisition specialist with 3 years running full-cycle recruiting for engineering and product roles.",
        "bullets": [
            "Closed 45+ engineering hires in a single year across junior to senior levels.",
            "Cut average time-to-hire from 42 to 27 days by streamlining the interview loop.",
            "Built a structured interview scorecard adopted company-wide.",
        ],
        "education": "BBA in Human Resources, Symbiosis Pune",
        "skills": "Full-Cycle Recruiting, ATS Tools, Sourcing, Interview Design",
        "stage": "Reject",
    },
    {
        "first_name": "Arjun",
        "last_name": "Rao",
        "job_title": "Marketing Executive",
        "phone": "+91 93210 98765",
        "note": "Marketing executive keen to grow awareness of open roles for a hiring platform.",
        "summary": "Marketing executive with experience running content and social campaigns for B2B products.",
        "bullets": [
            "Grew a company LinkedIn page from 2k to 15k followers in 10 months.",
            "Ran a content calendar that doubled inbound demo requests quarter over quarter.",
            "Managed a $50k/quarter paid social budget with a positive ROAS.",
        ],
        "education": "B.A. in Mass Communication, Delhi University",
        "skills": "Content Marketing, Social Media, SEO Basics, Campaign Analytics",
        "stage": "R1 Reject",
    },
    {
        "first_name": "Priya",
        "last_name": "Menon",
        "job_title": "Customer Success Associate",
        "phone": "+91 92109 87654",
        "note": "Customer success associate who enjoys helping users succeed with new products.",
        "summary": "Customer success associate experienced supporting SaaS customers through onboarding and renewal.",
        "bullets": [
            "Managed a portfolio of 80+ accounts with a 96% renewal rate.",
            "Cut average first-response time from 6 hours to 45 minutes.",
            "Built an onboarding checklist that reduced early-churn by 20%.",
        ],
        "education": "B.Com, Christ University, Bangalore",
        "skills": "Customer Onboarding, Zendesk, Account Management, Renewals",
        "stage": "Applied",
    },
]


def build_resume_pdf(path, candidate):
    name = f"{candidate['first_name']} {candidate['last_name']}"
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, name, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 7, f"{candidate['phone']}  |  {candidate['email']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, f"Applying for: {candidate['job_title']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, candidate["summary"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Experience", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)
    for bullet in candidate["bullets"]:
        pdf.multi_cell(0, 6, f"- {bullet}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Education", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, candidate["education"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "Skills", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, candidate["skills"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(path)


def main():
    health = requests.get(f"{API_URL}/health", timeout=10)
    health.raise_for_status()

    jobs = requests.get(f"{API_URL}/jobs", timeout=10).json()
    jobs_by_title = {j["title"]: j["id"] for j in jobs}

    login_resp = requests.post(
        f"{API_URL}/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}, timeout=10
    )
    login_resp.raise_for_status()
    token = login_resp.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    existing = requests.get(f"{API_URL}/applications", headers=auth_headers, timeout=10).json()
    existing_emails = {a["email"] for a in existing}

    os.makedirs(RESUME_DIR, exist_ok=True)

    results = []
    for candidate in CANDIDATES:
        candidate["email"] = f"{candidate['first_name'].lower()}.{candidate['last_name'].lower()}@example.com"

        job_id = jobs_by_title.get(candidate["job_title"])
        if not job_id:
            print(f"SKIP {candidate['first_name']} {candidate['last_name']}: job '{candidate['job_title']}' not found")
            continue

        if candidate["email"] in existing_emails:
            print(f"SKIP {candidate['first_name']} {candidate['last_name']}: already applied ({candidate['email']})")
            # still record for the summary table using existing data
            match = next(a for a in existing if a["email"] == candidate["email"])
            results.append((candidate["first_name"] + " " + candidate["last_name"], candidate["job_title"], match["stage"]))
            continue

        pdf_filename = f"{candidate['first_name'].lower()}_{candidate['last_name'].lower()}.pdf"
        pdf_path = os.path.join(RESUME_DIR, pdf_filename)
        build_resume_pdf(pdf_path, candidate)

        with open(pdf_path, "rb") as f:
            resp = requests.post(
                f"{API_URL}/applications",
                data={
                    "name": f"{candidate['first_name']} {candidate['last_name']}",
                    "phone": candidate["phone"],
                    "email": candidate["email"],
                    "job_id": job_id,
                    "note": candidate["note"],
                },
                files={"resume": (pdf_filename, f, "application/pdf")},
                timeout=30,
            )
        if resp.status_code != 201:
            print(f"FAILED to submit {candidate['first_name']} {candidate['last_name']}: {resp.status_code} {resp.text}")
            continue

        application = resp.json()
        target_stage = candidate["stage"]
        if target_stage != "Applied":
            stage_resp = requests.patch(
                f"{API_URL}/applications/{application['id']}/stage",
                json={"stage": target_stage},
                headers=auth_headers,
                timeout=10,
            )
            if stage_resp.status_code != 200:
                print(f"FAILED to set stage for {candidate['first_name']}: {stage_resp.status_code} {stage_resp.text}")
                target_stage = application["stage"]

        results.append((f"{candidate['first_name']} {candidate['last_name']}", candidate["job_title"], target_stage))
        print(f"OK {candidate['first_name']} {candidate['last_name']} -> {candidate['job_title']} [{target_stage}]")

    print("\nSummary")
    print("-------")
    for name, job_title, stage in results:
        print(f"{name:22s} {job_title:32s} {stage}")

    # Spot-check: fetch a resume URL for the first successfully created application
    check = requests.get(f"{API_URL}/applications", headers=auth_headers, timeout=10).json()
    demo_emails = {f"{c['first_name'].lower()}.{c['last_name'].lower()}@example.com" for c in CANDIDATES}
    demo_apps = [a for a in check if a["email"] in demo_emails]
    if demo_apps:
        sample = demo_apps[0]
        resume_resp = requests.get(
            f"{API_URL}/applications/{sample['id']}/resume", headers=auth_headers, timeout=10
        )
        print(f"\nResume spot-check for {sample['name']}: HTTP {resume_resp.status_code}, url present: {bool(resume_resp.json().get('url'))}")


if __name__ == "__main__":
    main()
