import sys
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

sys.path.append("..")
import database
from database import Figure, Tag, FigureTag
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("figures_api")

router = APIRouter()


# 添加请求模型
class CreateFigureRequest(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    tags: Optional[List[str]] = []
    status: Optional[str] = 'draft'


class UpdateFigureRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None


# 获取所有图表（支持分页）
@router.get("/figures")
def get_figures(page: int = 1, limit: int = 6, db: Session = Depends(database.get_db)):
    logger.info(f"收到获取图表数据的请求，页码: {page}, 每页数量: {limit}")
    try:
        # 计算偏移量
        offset = (page - 1) * limit
        
        # 获取总数量
        total_count = db.query(Figure).filter(Figure.status == 1).count()
        
        # 获取分页数据
        figures = db.query(Figure).filter(Figure.status == 1).offset(offset).limit(limit).all()
        logger.info(f"成功获取到 {len(figures)} 个已发布图表")

        # 转换为前端需要的格式
        figures_data = []
        for figure in figures:
            try:
                # 获取图表的标签
                figure_tags = db.query(Tag).join(FigureTag).filter(FigureTag.figure_id == figure.id).all()
                tags = [tag.name for tag in figure_tags]

                figure_dict = {
                    "id": figure.id,
                    "title": figure.title or "",
                    "description": figure.description or "",
                    "url": figure.url or "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg",  # 提供默认图床链接
                    "tags": tags
                }
                figures_data.append(figure_dict)
                logger.info(f"图表数据: ID={figure.id}, 标题={figure.title}")
            except Exception as e:
                logger.error(f"处理图表数据时发生错误 ID={figure.id}: {str(e)}")
                # 跳过有问题的数据，继续处理其他数据
                continue

        # 返回分页数据
        return {
            "data": figures_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "pages": (total_count + limit - 1) // limit  # 计算总页数
            }
        }
    except Exception as e:
        logger.error(f"获取图表数据时发生错误: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        # 返回空数据而不是抛出异常，避免前端报错
        return []


# 根据ID获取单个图表详情
@router.get("/figures/{figure_id}")
def get_figure_by_id(figure_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"收到获取图表详情的请求，ID: {figure_id}")
    try:
        figure = db.query(Figure).filter(Figure.id == figure_id, Figure.status == 1).first()
        if not figure:
            logger.warning(f"未找到图表，ID: {figure_id}")
            raise HTTPException(status_code=404, detail="图表未找到")

        # 获取图表的标签
        figure_tags = db.query(Tag).join(FigureTag).filter(FigureTag.figure_id == figure.id).all()
        tags = [tag.name for tag in figure_tags]

        figure_dict = {
            "id": figure.id,
            "title": figure.title or "",
            "description": figure.description or "",
            "url": figure.url or "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg",
            "tags": tags
        }

        logger.info(f"成功获取图表详情: {figure.title}")
        return figure_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取图表详情时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取图表详情时发生错误: {str(e)}")


# 获取所有图表标签及其图表数量
@router.get("/figure-tags")
def get_all_figure_tags(db: Session = Depends(database.get_db)):
    logger.info("收到获取所有图表标签的请求")
    try:
        all_tags = []
        tag_counts = {}

        # 获取所有已发布图表的标签统计
        figures = db.query(Figure).filter(Figure.status == 1).all()
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


# 管理员获取所有图片(包含所有状态)
@router.get("/admin/figures")
def get_all_figures_admin(db: Session = Depends(database.get_db)):
    logger.info("收到管理员获取全部图片数据的请求")
    try:
        figures = db.query(Figure).all()
        logger.info(f"成功获取到 {len(figures)} 张图片（所有状态）")

        # 转换为前端需要的格式
        figures_data = []
        for figure in figures:
            try:
                # 获取图片的标签
                figure_tags = db.query(Tag).join(FigureTag).filter(FigureTag.figure_id == figure.id).all()
                tags = [tag.name for tag in figure_tags]

                # 状态映射
                status_map = {0: 'draft', 1: 'published', 2: 'recycled'}

                figure_dict = {
                    "id": figure.id,
                    "title": figure.title or "",
                    "description": figure.description or "",
                    "url": figure.url or "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg",
                    "tags": tags,
                    "status": status_map.get(figure.status, 'draft')
                }
                figures_data.append(figure_dict)
                logger.info(f"图片数据: ID={figure.id}, 标题={figure.title}, 状态={figure.status}")
            except Exception as e:
                logger.error(f"处理图片数据时发生错误 ID={figure.id}: {str(e)}")
                continue

        return figures_data
    except Exception as e:
        logger.error(f"获取图片数据时发生错误: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        # 返回空数据而不是抛出异常
        return []


# 修改图片状态
@router.patch("/figures/{figure_id}/status")
def update_figure_status(figure_id: int, status_data: dict, db: Session = Depends(database.get_db)):
    logger.info(f"收到修改图片状态请求: ID={figure_id}, 状态={status_data.get('status')}")
    try:
        # 查找图片
        figure = db.query(Figure).filter(Figure.id == figure_id).first()
        if not figure:
            raise HTTPException(status_code=404, detail="图片未找到")

        # 状态映射
        status_map = {'draft': 0, 'published': 1, 'recycled': 2}
        new_status = status_data.get('status')

        if new_status not in status_map:
            raise HTTPException(status_code=400, detail="无效的状态值")

        # 更新状态
        old_status = figure.status
        figure.status = status_map[new_status]
        db.commit()

        logger.info(f"成功修改图片状态: {figure.title}, {old_status} -> {figure.status}")
        return {"message": "图片状态修改成功", "status": new_status}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"修改图片状态时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"修改图片状态时发生错误: {str(e)}")


# 删除图片
@router.delete("/figures/{figure_id}")
def delete_figure(figure_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"收到删除图片请求: ID={figure_id}")
    try:
        # 查找图片
        figure = db.query(Figure).filter(Figure.id == figure_id).first()
        if not figure:
            raise HTTPException(status_code=404, detail="图片未找到")

        # 删除图片-标签关联
        db.query(FigureTag).filter(FigureTag.figure_id == figure_id).delete()

        # 删除图片记录
        db.delete(figure)
        db.commit()

        logger.info(f"成功删除图片: {figure.title}")
        return {"message": "图片删除成功"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除图片时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除图片时发生错误: {str(e)}")


# 创建新图片
@router.post("/admin/figures")
def create_figure(figure_data: CreateFigureRequest, db: Session = Depends(database.get_db)):
    logger.info(f"收到创建图片请求: {figure_data.title}")
    try:
        # 状态映射
        status_map = {'draft': 0, 'published': 1, 'recycled': 2}
        status = status_map.get(figure_data.status, 0)

        # 验证URL格式
        import re
        url_pattern = r'^https?://.+\.(jpg|jpeg|png|gif|webp)(\?.*)?$'
        if not re.match(url_pattern, figure_data.url, re.IGNORECASE):
            logger.warning(f"图片URL格式不正确: {figure_data.url}")
            raise HTTPException(status_code=400, detail="请输入有效的图片URL（支持jpg、png、gif、webp格式）")

        # 创建图片记录
        new_figure = Figure(
            title=figure_data.title,
            description=figure_data.description,
            url=figure_data.url,
            status=status
        )

        db.add(new_figure)
        db.commit()
        db.refresh(new_figure)

        # 处理标签
        for tag_name in figure_data.tags or []:
            if not tag_name.strip():
                continue

            tag = db.query(Tag).filter(Tag.name == tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
                db.add(tag)
                db.flush()

            # 创建图片-标签关联
            figure_tag = FigureTag(figure_id=new_figure.id, tag_id=tag.id)
            db.add(figure_tag)

        db.commit()

        logger.info(f"成功创建图片: {new_figure.title}")
        return {
            "message": "图片上传成功",
            "id": new_figure.id,
            "url": new_figure.url
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建图片时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建图片时发生错误: {str(e)}")


# 编辑图片信息
@router.put("/admin/figures/{figure_id}")
def update_figure(figure_id: int, figure_data: UpdateFigureRequest, db: Session = Depends(database.get_db)):
    logger.info(f"收到编辑图片信息请求: ID={figure_id}")
    try:
        # 查找图片
        figure = db.query(Figure).filter(Figure.id == figure_id).first()
        if not figure:
            raise HTTPException(status_code=404, detail="图片未找到")

        # 更新图片信息
        if figure_data.title is not None:
            figure.title = figure_data.title
        if figure_data.description is not None:
            figure.description = figure_data.description
        if figure_data.url is not None:
            # 验证URL格式
            import re
            url_pattern = r'^https?://.+\.(jpg|jpeg|png|gif|webp)(\?.*)?$'
            if not re.match(url_pattern, figure_data.url, re.IGNORECASE):
                logger.warning(f"图片URL格式不正确: {figure_data.url}")
                raise HTTPException(status_code=400, detail="请输入有效的图片URL（支持jpg、png、gif、webp格式）")

            figure.url = figure_data.url
        if figure_data.status is not None:
            status_map = {'draft': 0, 'published': 1, 'recycled': 2}
            if figure_data.status in status_map:
                figure.status = status_map[figure_data.status]

        # 处理标签更新
        if figure_data.tags is not None:
            # 删除现有标签关联
            db.query(FigureTag).filter(FigureTag.figure_id == figure_id).delete()

            # 添加新标签
            for tag_name in figure_data.tags:
                if not tag_name.strip():
                    continue

                tag = db.query(Tag).filter(Tag.name == tag_name.strip()).first()
                if not tag:
                    tag = Tag(name=tag_name.strip())
                    db.add(tag)
                    db.flush()

                # 创建图片-标签关联
                figure_tag = FigureTag(figure_id=figure.id, tag_id=tag.id)
                db.add(figure_tag)

        db.commit()

        logger.info(f"成功编辑图片信息: {figure.title}")
        return {
            "message": "图片信息编辑成功",
            "id": figure.id,
            "title": figure.title
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"编辑图片信息时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"编辑图片信息时发生错误: {str(e)}")
