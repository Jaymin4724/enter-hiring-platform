import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.models.application import STAGES


class ApplicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_id: uuid.UUID
    name: str
    phone: str
    email: str
    resume_path: str
    note: str | None = None
    stage: str
    created_at: datetime
    updated_at: datetime


class StageUpdate(BaseModel):
    stage: str

    @field_validator("stage")
    @classmethod
    def stage_must_be_valid(cls, value: str) -> str:
        if value not in STAGES:
            raise ValueError(f"stage must be one of {STAGES}")
        return value
