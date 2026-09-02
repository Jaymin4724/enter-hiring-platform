"""One-off bootstrap: create the private Supabase Storage bucket for resumes.
Run with: ./venv/Scripts/python.exe setup_storage.py
"""

from app.services.storage import ensure_resume_bucket, RESUME_BUCKET

if __name__ == "__main__":
    ensure_resume_bucket()
    print(f"Bucket ready: {RESUME_BUCKET}")
