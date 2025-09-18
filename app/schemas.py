from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# 时间线基础模型
class TimelineBase(BaseModel):
    timestamp: datetime
    content: str


# 创建时间线的请求模型
class TimelineCreate(TimelineBase):
    pass


# 更新时间线的请求模型
class TimelineUpdate(BaseModel):
    timestamp: Optional[datetime] = None
    content: Optional[str] = None


# 时间线响应模型
class TimelineResponse(TimelineBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2
