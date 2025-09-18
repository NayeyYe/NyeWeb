import sys
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

sys.path.append("..")
import schemas, database
from database import Timeline
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("timeline_api")

router = APIRouter()

"""
直接从数据库获取时间线数据
模拟 test_timeline.py 中测试通过的数据获取方法
返回与测试相同的数据格式
"""
@router.get("/timeline/database")
def get_timeline_from_database(db: Session = Depends(database.get_db)) -> Dict[str, Any]:
    logger.info("收到从数据库直接获取时间线数据的请求")
    try:
        # 使用与 test_timeline.py 相同的查询方法
        timeline_items = db.query(Timeline).order_by(Timeline.timestamp.desc()).all()

        logger.info(f"从数据库获取到 {len(timeline_items)} 条数据")

        # 如果没有数据，返回空的成功响应
        if not timeline_items:
            logger.warning("数据库中没有时间线数据")
            return {
                "status": "success",
                "data": [],
                "total": 0,
                "message": "数据库中暂无时间线数据"
            }

        # 转换为字典格式，与 test_timeline.py 中的转换方式完全相同
        timeline_data = []
        for item in timeline_items:
            item_dict = {
                "id": item.id,
                "timestamp": item.timestamp.isoformat() if item.timestamp else None,
                "content": item.content
            }
            timeline_data.append(item_dict)
            logger.info(f"处理数据 - ID: {item.id}, 时间: {item.timestamp}, 内容: {item.content[:30]}...")

        # 模拟 test_timeline.py 中的 API 响应格式
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
        # 返回错误响应，保持格式一致
        return {
            "status": "error",
            "data": [],
            "total": 0,
            "message": f"获取时间线数据时发生错误: {str(e)}"
        }


# 修改基本时间线端点使用相同的数据格式
@router.get("/timeline")
def get_timeline(db: Session = Depends(database.get_db)):
    logger.info("收到获取时间线数据的请求")
    try:
        timeline_items = db.query(Timeline).order_by(Timeline.timestamp.desc()).all()
        logger.info(f"成功获取到 {len(timeline_items)} 条时间线数据")

        # 改用与上面相同的数据转换格式
        timeline_data = []
        for item in timeline_items:
            item_dict = {
                "id": item.id,
                "timestamp": item.timestamp.isoformat() if item.timestamp else None,
                "content": item.content
            }
            timeline_data.append(item_dict)
            logger.info(f"时间线数据: ID={item.id}, 时间={item.timestamp}, 内容={item.content[:30]}...")

        # 直接返回JSON数组，不使用response_model自动序列化
        return timeline_data
    except Exception as e:
        logger.error(f"获取时间线数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取时间线数据时发生错误: {str(e)}")


# 创建新的时间线条目

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


# 更新时间线条目

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

    # 修复：使用 model_dump 代替 dict
    update_data = timeline_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_timeline, field, value)

    db.commit()
    db.refresh(db_timeline)
    logger.info(f"成功更新时间线条目，ID: {db_timeline.id}")
    return db_timeline


# 删除时间线条目

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


# 添加请求模型
class CreateTimelineRequest(BaseModel):
    timestamp: str
    content: str


# 创建新的时间线项目

@router.post("/timeline")
def create_timeline_item(item_data: CreateTimelineRequest, db: Session = Depends(database.get_db)):
    logger.info(f"收到创建时间线项目请求: {item_data.content[:50]}...")
    try:
        # 解析时间戳
        try:
            timestamp = datetime.strptime(item_data.timestamp, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise HTTPException(status_code=400, detail="时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式")

        # 创建时间线记录
        new_timeline = Timeline(
            timestamp=timestamp,
            content=item_data.content
        )

        db.add(new_timeline)
        db.commit()
        db.refresh(new_timeline)

        logger.info(f"成功创建时间线项目: ID={new_timeline.id}")
        return {
            "message": "时间线项目创建成功",
            "id": new_timeline.id
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建时间线项目时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建时间线项目时发生错误: {str(e)}")


# 更新时间线项目
@router.put("/timeline/{timeline_id}")
def update_timeline_item(timeline_id: int, item_data: CreateTimelineRequest, db: Session = Depends(database.get_db)):
    logger.info(f"收到更新时间线项目请求: ID={timeline_id}")
    try:
        # 查找时间线项目
        timeline_item = db.query(Timeline).filter(Timeline.id == timeline_id).first()
        if not timeline_item:
            raise HTTPException(status_code=404, detail="时间线项目未找到")

        # 解析时间戳
        try:
            timestamp = datetime.strptime(item_data.timestamp, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise HTTPException(status_code=400, detail="时间格式错误，请使用 YYYY-MM-DD HH:MM:SS 格式")

        # 更新数据
        timeline_item.timestamp = timestamp
        timeline_item.content = item_data.content
        db.commit()

        logger.info(f"成功更新时间线项目: ID={timeline_id}")
        return {"message": "时间线项目更新成功"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"更新时间线项目时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"更新时间线项目时发生错误: {str(e)}")


# 删除时间线项目
@router.delete("/timeline/{timeline_id}")
def delete_timeline_item(timeline_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"收到删除时间线项目请求: ID={timeline_id}")
    try:
        # 查找时间线项目
        timeline_item = db.query(Timeline).filter(Timeline.id == timeline_id).first()
        if not timeline_item:
            raise HTTPException(status_code=404, detail="时间线项目未找到")

        # 删除记录
        db.delete(timeline_item)
        db.commit()

        logger.info(f"成功删除时间线项目: ID={timeline_id}")
        return {"message": "时间线项目删除成功"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除时间线项目时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除时间线项目时发生错误: {str(e)}")
