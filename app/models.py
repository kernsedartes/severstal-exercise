from datetime import date
from sqlalchemy import Column, Integer, Float, Date
from .database import Base

# Модель для рулона металла
class MetalRoll(Base):
    __tablename__ = "metal_rolls"

    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    added_date = Column(Date, default=date.today())
    removed_date = Column(Date, nullable=True)