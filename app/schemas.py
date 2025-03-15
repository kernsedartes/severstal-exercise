from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class MetalRollCreate(BaseModel):
    length: float
    weight: float


class MetalRollResponse(BaseModel):
    id: int
    length: float
    weight: float
    added_date: datetime
    removed_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class StatsRequest(BaseModel):
    start_date: str
    end_date: str = None
