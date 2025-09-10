from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TimelineBase(BaseModel):
    timestamp: datetime
    content: str


class TimelineCreate(TimelineBase):
    pass


class TimelineUpdate(BaseModel):
    timestamp: Optional[datetime] = None
    content: Optional[str] = None


class TimelineResponse(TimelineBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2
        orm_mode = True  # Pydantic v1 兼容
