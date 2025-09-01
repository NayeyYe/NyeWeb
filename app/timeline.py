from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas, database
from database import Timeline
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("timeline_api")

router = APIRouter()

# 获取所有时间线条目
@router.get("/timeline", response_model=List[schemas.TimelineResponse])
def get_timeline(db: Session = Depends(database.get_db)):
    """获取所有时间线条目，按时间倒序排列"""
    logger.info("收到获取时间线数据的请求")
    try:
        timeline_items = db.query(Timeline).order_by(Timeline.timestamp.desc()).all()
        logger.info(f"成功获取到 {len(timeline_items)} 条时间线数据")
        return timeline_items
    except Exception as e:
        logger.error(f"获取时间线数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取时间线数据时发生错误: {str(e)}")

# 创建新的时间线条目
@router.post("/timeline", response_model=schemas.TimelineResponse)
def create_timeline_item(
    timeline_item: schemas.TimelineCreate,
    db: Session = Depends(database.get_db)
):
    """创建新的时间线条目"""
    logger.info("收到创建时间线条目的请求")
    try:
        db_timeline = Timeline(
            timestamp=timeline_item.timestamp,
            content=timeline_item.content
        )
        db.add(db_timeline)
        db.commit()
        db.refresh(db_timeline)
        logger.info(f"成功创建时间线条目，ID: {db_timeline.id}")
        return db_timeline
    except Exception as e:
        logger.error(f"创建时间线条目时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建时间线条目时发生错误: {str(e)}")

# 更新时间线条目
@router.put("/timeline/{item_id}", response_model=schemas.TimelineResponse)
def update_timeline_item(
    item_id: int,
    timeline_update: schemas.TimelineUpdate,
    db: Session = Depends(database.get_db)
):
    """更新指定ID的时间线条目"""
    logger.info(f"收到更新时间线条目的请求，ID: {item_id}")
    db_timeline = db.query(Timeline).filter(Timeline.id == item_id).first()
    if not db_timeline:
        logger.warning(f"尝试更新不存在的时间线条目，ID: {item_id}")
        raise HTTPException(status_code=404, detail="Timeline item not found")

    update_data = timeline_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_timeline, field, value)

    db.commit()
    db.refresh(db_timeline)
    logger.info(f"成功更新时间线条目，ID: {db_timeline.id}")
    return db_timeline

# 删除时间线条目
@router.delete("/timeline/{item_id}")
def delete_timeline_item(item_id: int, db: Session = Depends(database.get_db)):
    """删除指定ID的时间线条目"""
    logger.info(f"收到删除时间线��目的请求，ID: {item_id}")
    db_timeline = db.query(Timeline).filter(Timeline.id == item_id).first()
    if not db_timeline:
        logger.warning(f"尝试删除不存在的时间线条目，ID: {item_id}")
        raise HTTPException(status_code=404, detail="Timeline item not found")

    db.delete(db_timeline)
    db.commit()
    logger.info(f"成功删除时间线条目，ID: {item_id}")
    return {"message": "Timeline item deleted successfully"}
