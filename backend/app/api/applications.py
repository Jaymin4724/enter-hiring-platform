import re
import uuid

from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import Admin, Application, Job
from app.models.application import DEFAULT_STAGE, STAGES
from app.schemas.application import ApplicationOut, StageUpdate
from app.services.auth import get_current_admin
from app.services.storage import InvalidResumeError, get_resume_signed_url, upload_resume

router = APIRouter(prefix="/applications", tags=["applications"])

PHONE_PATTERN = re.compile(r"^\+?[0-9 ()-]{7,20}$")


def _get_application_or_404(application_id: uuid.UUID, db: Session) -> Application:
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.post("", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def submit_application(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    job_id: uuid.UUID = Form(...),
    note: str | None = Form(None),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not db.get(Job, job_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid email address")

    if not PHONE_PATTERN.match(phone):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid phone number")

    application_id = uuid.uuid4()
    try:
        resume_path = upload_resume(resume, application_id)
    except InvalidResumeError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc))

    application = Application(
        id=application_id,
        job_id=job_id,
        name=name,
        phone=phone,
        email=email,
        resume_path=resume_path,
        note=note,
        stage=DEFAULT_STAGE,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("", response_model=list[ApplicationOut])
def list_applications(
    job_id: uuid.UUID | None = None,
    stage: str | None = None,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    query = db.query(Application)
    if job_id:
        query = query.filter(Application.job_id == job_id)
    if stage:
        if stage not in STAGES:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid stage")
        query = query.filter(Application.stage == stage)
    return query.order_by(Application.created_at.desc()).all()


@router.patch("/{application_id}/stage", response_model=ApplicationOut)
def update_stage(
    application_id: uuid.UUID,
    payload: StageUpdate,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    application = _get_application_or_404(application_id, db)
    application.stage = payload.stage
    db.commit()
    db.refresh(application)
    return application


@router.get("/{application_id}/resume")
def get_resume(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(get_current_admin),
):
    application = _get_application_or_404(application_id, db)
    return {"url": get_resume_signed_url(application.resume_path)}
