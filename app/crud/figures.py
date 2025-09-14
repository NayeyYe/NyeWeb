import sys

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.append("..")
import database
from database import Figure, Tag, FigureTag
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("figures_api")

router = APIRouter()

@router.get("/figures")
def get_figures(db: Session = Depends(database.get_db)):
    """获取所有图表"""
    logger.info("收到获取图表数据的请求")
    try:
        figures = db.query(Figure).all()
        logger.info(f"成功获取到 {len(figures)} 个图表")

        # 转换为前端需要的格式
        figures_data = []
        for figure in figures:
            # 获取图表的标签
            figure_tags = db.query(Tag).join(FigureTag).filter(FigureTag.figure_id == figure.id).all()
            tags = [tag.name for tag in figure_tags]

            figure_dict = {
                "id": figure.id,
                "title": figure.title,
                "description": figure.description,
                "filename": figure.filename,
                "tags": tags
            }
            figures_data.append(figure_dict)
            logger.info(f"图表数据: ID={figure.id}, 标题={figure.title}")

        return figures_data
    except Exception as e:
        logger.error(f"获取图表数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取图表数据时发生错误: {str(e)}")

@router.get("/figures/{figure_id}")
def get_figure_by_id(figure_id: int, db: Session = Depends(database.get_db)):
    """根据ID获取单个图表详情"""
    logger.info(f"收到获取图表详情的请求，ID: {figure_id}")
    try:
        figure = db.query(Figure).filter(Figure.id == figure_id).first()
        if not figure:
            logger.warning(f"未找到图表，ID: {figure_id}")
            raise HTTPException(status_code=404, detail="图表未找到")

        # 获取图表的标签
        figure_tags = db.query(Tag).join(FigureTag).filter(FigureTag.figure_id == figure.id).all()
        tags = [tag.name for tag in figure_tags]

        figure_dict = {
            "id": figure.id,
            "title": figure.title,
            "description": figure.description,
            "filename": figure.filename,
            "tags": tags
        }

        logger.info(f"成功获取图表详情: {figure.title}")
        return figure_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取图表详情时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取图表详情时发生错误: {str(e)}")

@router.get("/figure-tags")
def get_all_figure_tags(db: Session = Depends(database.get_db)):
    """获取所有图表标签及其图表数量"""
    logger.info("收到获取所有图表标签的请求")
    try:
        all_tags = []
        tag_counts = {}

        # 获取所有图表的标签统计
        figures = db.query(Figure).all()
        for figure in figures:
            figure_tags = db.query(Tag).join(FigureTag).filter(FigureTag.figure_id == figure.id).all()
            for tag in figure_tags:
                if tag.name not in all_tags:
                    all_tags.append(tag.name)
                tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1

        logger.info(f"成功获取 {len(all_tags)} 个图表标签")
        return {
            "tags": all_tags,
            "counts": tag_counts
        }
    except Exception as e:
        logger.error(f"获取图表标签时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取图表标签时发生错误: {str(e)}")

