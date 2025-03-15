from datetime import date
from pydantic import BaseModel
from typing import Optional


class MetalRollCreate(BaseModel):
    length: float
    weight: float


class MetalRollResponse(BaseModel):
    id: int
    length: float
    weight: float
    added_date: date
    removed_date: Optional[date] = None

    class Config:
        from_attributes = True


class StatsRequest(BaseModel):
    start_date: str
    end_date: str = None
