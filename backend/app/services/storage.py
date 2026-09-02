from supabase import create_client, Client

from app.core.config import settings

RESUME_BUCKET = "resumes"


def get_supabase_admin_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def ensure_resume_bucket() -> None:
    client = get_supabase_admin_client()
    existing = {b.name for b in client.storage.list_buckets()}
    if RESUME_BUCKET not in existing:
        client.storage.create_bucket(RESUME_BUCKET, options={"public": False})
