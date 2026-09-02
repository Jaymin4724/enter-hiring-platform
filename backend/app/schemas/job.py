import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class JobWrite(BaseModel):
    title: str = Field(..., max_length=200)
    department: str | None = Field(None, max_length=120)
    location: str | None = Field(None, max_length=120)
    description: str | None = Field(None, max_length=5000)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title is required.")
        return value

    @field_validator("department", "location", "description")
    @classmethod
    def strip_optional_fields(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        return value or None


class JobCreate(JobWrite):
    pass


class JobUpdate(JobWrite):
    pass


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    department: str | None = None
    location: str | None = None
    description: str | None = None
    created_at: datetime
