from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from .database import Base


class MetalRoll(Base):
    __tablename__ = "metal_rolls"

    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    added_date = Column(DateTime, default=datetime.now())
    removed_date = Column(DateTime, nullable=True)
