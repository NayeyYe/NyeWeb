import sys
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.append("..")
import schemas, database
from database import Timeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("timeline_api")

router = APIRouter()


@router.get("/timeline/database")
def get_timeline_from_database(db: Session = Depends(database.get_db)) -> Dict[str, Any]:
    logger.info("收到从数据库直接获取时间线数据的请求")
    try:

        timeline_items = db.query(Timeline).order_by(Timeline.timestamp.desc()).all()

        logger.info(f"从数据库获取到 {len(timeline_items)} 条数据")

        if not timeline_items:
            logger.warning("数据库中没有时间线数据")
            return {
                "status": "success",
                "data": [],
                "total": 0,
                "message": "数据库中暂无时间线数据"
            }

        timeline_data = []
        for item in timeline_items:
            item_dict = {
                "id": item.id,
                "timestamp": item.timestamp.isoformat() if item.timestamp else None,
                "content": item.content
            }
            timeline_data.append(item_dict)
            logger.info(f"处理数据 - ID: {item.id}, 时间: {item.timestamp}, 内容: {item.content[:30]}...")

        api_response = {
            "status": "success",
            "data": timeline_data,
            "total": len(timeline_data),
            "message": f"成功获取 {len(timeline_data)} 条时间线数据"
        }

        logger.info(f"成功处理 {len(timeline_data)} 条记录，返回API响应")
        logger.info(f"返回的数据: {timeline_data}")
        return api_response

    except Exception as e:
        logger.error(f"从数据库获取时间线数据时发生错误: {str(e)}")
        import traceback
        logger.error(f"详细错误堆栈: {traceback.format_exc()}")

        return {
            "status": "error",
            "data": [],
            "total": 0,
            "message": f"获取时间线数据时发生错误: {str(e)}"
        }


@router.get("/timeline")
def get_timeline(db: Session = Depends(database.get_db)):
    logger.info("收到获取时间线数据的请求")
    try:
        timeline_items = db.query(Timeline).order_by(Timeline.timestamp.desc()).all()
        logger.info(f"成功获取到 {len(timeline_items)} 条时间线数据")

        timeline_data = []
        for item in timeline_items:
            item_dict = {
                "id": item.id,
                "timestamp": item.timestamp.isoformat() if item.timestamp else None,
                "content": item.content
            }
            timeline_data.append(item_dict)
            logger.info(f"时间线数据: ID={item.id}, 时间={item.timestamp}, 内容={item.content[:30]}...")

        return timeline_data
    except Exception as e:
        logger.error(f"获取时间线数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取时间线数据时发生错误: {str(e)}")


@router.post("/timeline", response_model=schemas.TimelineResponse)
def create_timeline_item(
        timeline_item: schemas.TimelineCreate,
        db: Session = Depends(database.get_db)
):
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


@router.put("/timeline/{item_id}", response_model=schemas.TimelineResponse)
def update_timeline_item(
        item_id: int,
        timeline_update: schemas.TimelineUpdate,
        db: Session = Depends(database.get_db)
):
    logger.info(f"收到更新时间线条目的请求，ID: {item_id}")
    db_timeline = db.query(Timeline).filter(Timeline.id == item_id).first()
    if not db_timeline:
        logger.warning(f"尝试更新不存在的时间线条目，ID: {item_id}")
        raise HTTPException(status_code=404, detail="Timeline item not found")

    update_data = timeline_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_timeline, field, value)

    db.commit()
    db.refresh(db_timeline)
    logger.info(f"成功更新时间线条目，ID: {db_timeline.id}")
    return db_timeline


@router.delete("/timeline/{item_id}")
def delete_timeline_item(item_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"收到删除时间线条目的请求，ID: {item_id}")
    db_timeline = db.query(Timeline).filter(Timeline.id == item_id).first()
    if not db_timeline:
        logger.warning(f"尝试删除不存在的时间线条目，ID: {item_id}")
        raise HTTPException(status_code=404, detail="Timeline item not found")

    db.delete(db_timeline)
    db.commit()
    logger.info(f"成功删除时间线条目，ID: {item_id}")
    return {"message": "Timeline item deleted successfully"}
