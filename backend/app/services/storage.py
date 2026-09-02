import mimetypes
import uuid

from fastapi import UploadFile
from supabase import create_client, Client

from app.core.config import settings

RESUME_BUCKET = "resumes"

ALLOWED_RESUME_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def get_supabase_admin_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


def ensure_resume_bucket() -> None:
    client = get_supabase_admin_client()
    existing = {b.name for b in client.storage.list_buckets()}
    if RESUME_BUCKET not in existing:
        client.storage.create_bucket(RESUME_BUCKET, options={"public": False})


class InvalidResumeError(ValueError):
    pass


def upload_resume(file: UploadFile, application_id: uuid.UUID) -> str:
    if file.content_type not in ALLOWED_RESUME_CONTENT_TYPES:
        raise InvalidResumeError("Resume must be a PDF or Word document")

    contents = file.file.read()
    if len(contents) > MAX_RESUME_SIZE_BYTES:
        raise InvalidResumeError("Resume file must be 5MB or smaller")

    extension = mimetypes.guess_extension(file.content_type) or ""
    path = f"{application_id}{extension}"

    client = get_supabase_admin_client()
    client.storage.from_(RESUME_BUCKET).upload(
        path, contents, {"content-type": file.content_type}
    )
    return path


def get_resume_signed_url(path: str, expires_in: int = 3600) -> str:
    client = get_supabase_admin_client()
    result = client.storage.from_(RESUME_BUCKET).create_signed_url(path, expires_in)
    return result.get("signedURL") or result.get("signed_url")


def delete_resume(path: str) -> None:
    client = get_supabase_admin_client()
    client.storage.from_(RESUME_BUCKET).remove([path])
