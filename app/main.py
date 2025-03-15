import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from app.models import MetalRoll
from app.schemas import MetalRollCreate, MetalRollResponse, StatsRequest
from app.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/rolls/", response_model=MetalRollResponse)
async def create_roll(roll: MetalRollCreate, db: Session=Depends(get_db)):
    db_roll = MetalRoll(**roll.dict())
    db.add(db_roll)
    db.commit()
    db.refresh(db_roll)
    return db_roll


@app.delete("/rolls/{roll_id}", response_model=MetalRollResponse)
async def delete_roll(roll_id: int, db: Session=Depends(get_db)):
    db_roll = db.query(MetalRoll).filter(MetalRoll.id == roll_id).first()
    if db_roll is None:
        raise HTTPException(status_code=404, detail="Roll not found")
    if db_roll.removed_date is None or db_roll.removed_date == "null":
        db_roll.removed_date = datetime.now()
        db.commit()
        db.refresh(db_roll)
        return db_roll
    else:
        raise HTTPException(status_code=404, detail="Roll is already deleted")


@app.get("/getrolls/", response_model=List[MetalRollResponse])
async def get_rolls(
    id_range: Optional[str]=None,
    weight_range: Optional[str]=None,
    length_range: Optional[str]=None,
    added_date_range: Optional[str]=None,
    removed_date_range: Optional[str]=None,
    db: Session=Depends(get_db)
):
    query = db.query(MetalRoll)

    if id_range:
        start, end = map(int, id_range.split("-"))
        query = query.filter(MetalRoll.id.between(start, end))

    if weight_range:
        start, end = map(float, weight_range.split("-"))
        query = query.filter(MetalRoll.weight.between(start, end))

    if length_range:
        start, end = map(float, length_range.split("-"))
        query = query.filter(MetalRoll.length.between(start, end))

    if added_date_range:
        start, end = map(lambda x: datetime.fromisoformat(x),
                         added_date_range.split("/"))
        query = query.filter(MetalRoll.added_date.between(start, end))

    if removed_date_range:
        start, end = map(lambda x: datetime.fromisoformat(x),
                         removed_date_range.split("/"))
        query = query.filter(MetalRoll.removed_date.between(start, end))

    return query.all()


@app.post("/stats/")
async def get_stats(stats_request: StatsRequest,
                    db: Session=Depends(get_db)):

    try:
        start_date = datetime.fromisoformat(stats_request.start_date)
        end_date = (datetime.fromisoformat(stats_request.end_date)
                    if stats_request.end_date else datetime.now())
    except ValueError as e:
        raise HTTPException(status_code=400,
                            detail=f'Invalid date format: {e}')

    rolls = (db.query(MetalRoll).filter(MetalRoll.
             added_date.between(start_date, end_date)).all())

    added_rolls = len([roll for roll in rolls if roll.added_date >=
                       start_date and roll.added_date <= end_date])

    removed_rolls = len([roll for roll in rolls if roll.removed_date and
                         roll.added_date >= start_date and
                         roll.added_date <= end_date])

    lengths = [roll.length for roll in rolls]
    weights = [roll.weight for roll in rolls]

    avg_length = sum(lengths) / len(lengths) if lengths else 0
    avg_weight = sum(weights) / len(weights) if weights else 0

    max_length = max(lengths) if lengths else 0
    min_length = min(lengths) if lengths else 0

    max_weight = max(weights) if weights else 0
    min_weight = min(weights) if weights else 0

    total_weight = sum(weights)

    time_diffs = [
        (roll.removed_date - roll.added_date).total_seconds()
        for roll in rolls if roll.removed_date and
        roll.added_date >= start_date and
        roll.added_date <= end_date
    ]

    if time_diffs:
        max_time_diff = max(time_diffs)
        min_time_diff = min(time_diffs)
    else:
        max_time_diff = 0
        min_time_diff = 0

    return {
        "added_rolls": added_rolls,
        "removed_rolls": removed_rolls,
        "avg_length": avg_length,
        "avg_weight": avg_weight,
        "max_length": max_length,
        "min_length": min_length,
        "max_weight": max_weight,
        "min_weight": min_weight,
        "total_weight": total_weight,
        "len_time_diffs": len(time_diffs),
        "max_time_diff": max_time_diff,
        "min_time_diff": min_time_diff,
    }


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
