import sys

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.append("..")
import database
from database import Project, Tag, ProjectTag
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("projects_api")

router = APIRouter()

@router.get("/projects")
def get_projects(db: Session = Depends(database.get_db)):
    """获取所有项目，按日期倒序排列"""
    logger.info("收到获取项目数据的请求")
    try:
        projects = db.query(Project).order_by(Project.date.desc()).all()
        logger.info(f"成功获取到 {len(projects)} 个项目")

        # 转换为前端需要的格式
        projects_data = []
        for project in projects:
            # 获取项目的标签
            project_tags = db.query(Tag).join(ProjectTag).filter(ProjectTag.project_id == project.id).all()
            tags = [tag.name for tag in project_tags]

            project_dict = {
                "id": project.id,
                "title": project.title,
                "slug": project.slug,
                "summary": project.summary,
                "date": project.date.strftime('%Y-%m-%d') if project.date else None,
                "tags": tags
            }
            projects_data.append(project_dict)
            logger.info(f"项目数据: ID={project.id}, 标题={project.title}")

        return projects_data
    except Exception as e:
        logger.error(f"获取项目数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取项目数据时发生错误: {str(e)}")

@router.get("/projects/{project_slug}")
def get_project_by_slug(project_slug: str, db: Session = Depends(database.get_db)):
    """根据slug获取单个项目详情"""
    logger.info(f"收到获取项目详情的请求，slug: {project_slug}")
    try:
        project = db.query(Project).filter(Project.slug == project_slug).first()
        if not project:
            logger.warning(f"未找到项目，slug: {project_slug}")
            raise HTTPException(status_code=404, detail="项目未找到")

        # 获取项目的标签
        project_tags = db.query(Tag).join(ProjectTag).filter(ProjectTag.project_id == project.id).all()
        tags = [tag.name for tag in project_tags]

        project_dict = {
            "id": project.id,
            "title": project.title,
            "slug": project.slug,
            "summary": project.summary,
            "date": project.date.strftime('%Y-%m-%d') if project.date else None,
            "tags": tags
        }

        logger.info(f"成功获取项目详情: {project.title}")
        return project_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取项目详情时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取项目详情时发生错误: {str(e)}")

@router.get("/project-tags")
def get_all_project_tags(db: Session = Depends(database.get_db)):
    """获取所有项目标签及其项目数量"""
    logger.info("收到获取所有项目标签的请求")
    try:
        # 简化处理，直接获取所有项目标签和计数
        all_tags = []
        tag_counts = {}

        # 获取所有项目的标签统计
        projects = db.query(Project).all()
        for project in projects:
            project_tags = db.query(Tag).join(ProjectTag).filter(ProjectTag.project_id == project.id).all()
            for tag in project_tags:
                if tag.name not in all_tags:
                    all_tags.append(tag.name)
                tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1

        logger.info(f"成功获取 {len(all_tags)} 个项目标签")
        return {
            "tags": all_tags,
            "counts": tag_counts
        }
    except Exception as e:
        logger.error(f"获取项目标签时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取项目标签时发生错误: {str(e)}")
