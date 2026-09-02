"""One-off bootstrap: seed 10 sample jobs and the admin account.
Run with: ./venv/Scripts/python.exe seed.py
"""

import bcrypt

from app.core.db import SessionLocal
from app.models import Job, Admin

ADMIN_EMAIL = "admin@enter.in"
ADMIN_PASSWORD = "Enter@Hiring2026"

JOBS = [
    {
        "title": "Backend Engineer",
        "department": "Engineering",
        "location": "Bangalore",
        "description": "Build and maintain the core hiring platform API.",
    },
    {
        "title": "Frontend Engineer",
        "department": "Engineering",
        "location": "Bangalore",
        "description": "Own the candidate and admin-facing React apps.",
    },
    {
        "title": "DevOps Engineer",
        "department": "Engineering",
        "location": "Remote",
        "description": "Own deployments, CI/CD, and infrastructure reliability.",
    },
    {
        "title": "QA Engineer",
        "department": "Engineering",
        "location": "Bangalore",
        "description": "Test coverage and release quality across the platform.",
    },
    {
        "title": "Product Manager",
        "department": "Product",
        "location": "Remote",
        "description": "Define and prioritize the hiring platform roadmap.",
    },
    {
        "title": "UI/UX Designer",
        "department": "Design",
        "location": "Bangalore",
        "description": "Design simple, fast flows for candidates and admins.",
    },
    {
        "title": "Data Analyst",
        "department": "Data",
        "location": "Bangalore",
        "description": "Track hiring funnel metrics and build reporting.",
    },
    {
        "title": "Talent Acquisition Specialist",
        "department": "HR",
        "location": "Bangalore",
        "description": "Run the day-to-day hiring pipeline for open roles.",
    },
    {
        "title": "Marketing Executive",
        "department": "Marketing",
        "location": "Remote",
        "description": "Grow awareness of open roles and the employer brand.",
    },
    {
        "title": "Customer Success Associate",
        "department": "Customer Success",
        "location": "Bangalore",
        "description": "Support customers using the platform post-launch.",
    },
]


def seed():
    db = SessionLocal()
    try:
        if db.query(Job).count() == 0:
            db.add_all([Job(**job) for job in JOBS])
            print(f"Inserted {len(JOBS)} jobs.")
        else:
            print("Jobs already present, skipping.")

        if not db.query(Admin).filter_by(email=ADMIN_EMAIL).first():
            password_hash = bcrypt.hashpw(ADMIN_PASSWORD.encode(), bcrypt.gensalt()).decode()
            db.add(Admin(email=ADMIN_EMAIL, password_hash=password_hash))
            print(f"Inserted admin account: {ADMIN_EMAIL}")
        else:
            print("Admin already present, skipping.")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
