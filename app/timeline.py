from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, database
from .database import Timeline

router = APIRouter()

# 获取所有时间线条目
@router.get("/timeline", response_model=List[schemas.TimelineResponse])
def get_timeline(db: Session = Depends(database.get_db)):
    """获取所有时间线条目，按时间倒序排列"""
    timeline_items = db.query(Timeline).order_by(Timeline.timestamp.desc()).all()
    return timeline_items

# 创建新的时间线条目
@router.post("/timeline", response_model=schemas.TimelineResponse)
def create_timeline_item(
    timeline_item: schemas.TimelineCreate,
    db: Session = Depends(database.get_db)
):
    """创建新的时间线条目"""
    db_timeline = Timeline(
        timestamp=timeline_item.timestamp,
        content=timeline_item.content
    )
    db.add(db_timeline)
    db.commit()
    db.refresh(db_timeline)
    return db_timeline

# 更新时间线条目
@router.put("/timeline/{item_id}", response_model=schemas.TimelineResponse)
def update_timeline_item(
    item_id: int,
    timeline_update: schemas.TimelineUpdate,
    db: Session = Depends(database.get_db)
):
    """更新指定ID的时间线条目"""
    db_timeline = db.query(Timeline).filter(Timeline.id == item_id).first()
    if not db_timeline:
        raise HTTPException(status_code=404, detail="Timeline item not found")

    update_data = timeline_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_timeline, field, value)

    db.commit()
    db.refresh(db_timeline)
    return db_timeline

# 删除时间线条目
@router.delete("/timeline/{item_id}")
def delete_timeline_item(item_id: int, db: Session = Depends(database.get_db)):
    """删除指定ID的时间线条目"""
    db_timeline = db.query(Timeline).filter(Timeline.id == item_id).first()
    if not db_timeline:
        raise HTTPException(status_code=404, detail="Timeline item not found")

    db.delete(db_timeline)
    db.commit()
    return {"message": "Timeline item deleted successfully"}
