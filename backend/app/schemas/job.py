import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    title: str
    department: str | None = None
    location: str | None = None
    description: str | None = None


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class JobOut(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
