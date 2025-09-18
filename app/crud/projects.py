import os
import re
import sys
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

sys.path.append("..")
import database
from database import Project, Tag, ProjectTag
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("projects_api")

router = APIRouter()


# ===== REQUEST MODELS =====
class CreateProjectRequest(BaseModel):
    title: str
    slug: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = []
    status: Optional[str] = 'draft'
    content: str
    date: Optional[str] = None


class UpdateProjectRequest(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    content: Optional[str] = None
    date: Optional[str] = None


# 获取所有项目，按日期倒序排列
@router.get("/projects")
def get_projects(db: Session = Depends(database.get_db)):
    logger.info("收到获取项目数据的请求")
    try:
        projects = db.query(Project).filter(Project.status == 1).order_by(Project.date.desc()).all()
        logger.info(f"成功获取到 {len(projects)} 个已发布项目")

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


# 根据slug获取单个项目详情
@router.get("/projects/{project_slug}")
def get_project_by_slug(project_slug: str, db: Session = Depends(database.get_db)):
    logger.info(f"收到获取项目详情的请求，slug: {project_slug}")
    try:
        project = db.query(Project).filter(Project.slug == project_slug, Project.status == 1).first()
        if not project:
            logger.warning(f"未找到项目，slug: {project_slug}")
            raise HTTPException(status_code=404, detail="项目未找到")

        # 获取项目的title
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


# 获取所有项目标签及其项目数量
@router.get("/project-tags")
def get_all_project_tags(db: Session = Depends(database.get_db)):
    logger.info("收到获取所有项目标签的请求")
    try:
        all_tags = []
        tag_counts = {}

        # 获取所有已发布项目的标签统计
        projects = db.query(Project).filter(Project.status == 1).all()
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


# 管理员获取所有项目(包含所有状态)，按日期倒序排列
@router.get("/admin/projects")
def get_all_projects_admin(db: Session = Depends(database.get_db)):
    logger.info("收到管理员获取全部项目数据的请求")
    try:
        projects = db.query(Project).order_by(Project.date.desc()).all()
        logger.info(f"成功获取到 {len(projects)} 个项目（所有状态）")

        # 转换为前端需要的格式
        projects_data = []
        for project in projects:
            # 获取项目的标签
            project_tags = db.query(Tag).join(ProjectTag).filter(ProjectTag.project_id == project.id).all()
            tags = [tag.name for tag in project_tags]

            # 状态映射
            status_map = {0: 'draft', 1: 'published', 2: 'recycled'}

            project_dict = {
                "id": project.id,
                "title": project.title,
                "slug": project.slug,
                "summary": project.summary,
                "date": project.date.strftime('%Y-%m-%d') if project.date else None,
                "tags": tags,
                "status": status_map.get(project.status, 'draft')
            }
            projects_data.append(project_dict)
            logger.info(f"项目数据: ID={project.id}, 标题={project.title}, 状态={project.status}")

        return projects_data
    except Exception as e:
        logger.error(f"获取项目数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取项目数据时发生错误: {str(e)}")


# 修改项目状态
@router.patch("/projects/{project_id}/status")
def update_project_status(project_id: int, status_data: dict, db: Session = Depends(database.get_db)):
    logger.info(f"收到修改项目状态请求: ID={project_id}, 状态={status_data.get('status')}")
    try:
        # 查找项目
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="项目未找到")

        # 状态映射
        status_map = {'draft': 0, 'published': 1, 'recycled': 2}
        new_status = status_data.get('status')

        if new_status not in status_map:
            raise HTTPException(status_code=400, detail="无效的状态值")

        # 更新状态
        old_status = project.status
        project.status = status_map[new_status]
        db.commit()

        logger.info(f"成功修改项目状态: {project.title}, {old_status} -> {project.status}")
        return {"message": "项目状态修改成功", "status": new_status}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"修改项目状态时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"修改项目状态时发生错误: {str(e)}")


# 项目管理api
# 创建新项目
@router.post("/projects")
def create_project(project_data: CreateProjectRequest, db: Session = Depends(database.get_db)):
    logger.info(f"收到创建项目请求: {project_data.title}")
    try:
        # 生成或验证slug，自动从标题生成
        if not project_data.slug:
            slug = generate_safe_slug(project_data.title)
        else:
            slug = generate_safe_slug(project_data.slug)

        # 确保slug唯一性
        base_slug = slug
        counter = 1
        while db.query(Project).filter(Project.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # 解析日期
        project_date = datetime.now().date()
        if project_data.date:
            try:
                project_date = datetime.strptime(project_data.date, '%Y-%m-%d').date()
            except ValueError:
                logger.warning(f"日期格式错误，使用当前日期: {project_data.date}")

        # 状态映射
        status_map = {'draft': 0, 'published': 1, 'recycled': 2}
        status = status_map.get(project_data.status, 0)

        # 创建项目记录
        new_project = Project(
            title=project_data.title,
            slug=slug,
            summary=project_data.summary,
            date=project_date,
            status=status
        )

        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        # 处理标签
        for tag_name in project_data.tags or []:
            if not tag_name.strip():
                continue

            tag = db.query(Tag).filter(Tag.name == tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
                db.add(tag)
                db.flush()

            # 创建项目-标签关联
            project_tag = ProjectTag(project_id=new_project.id, tag_id=tag.id)
            db.add(project_tag)

        db.commit()

        # 保存项目markdown文件
        try:
            save_project_file(new_project, project_data.content)
        except Exception as e:
            logger.warning(f"保存项目文件失败: {str(e)}")

        logger.info(f"成功创建项目: {new_project.title}")
        return {
            "message": "项目上传成功",
            "id": new_project.id,
            "slug": new_project.slug
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建项目时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建项目时发生错误: {str(e)}")


# 编辑项目信息
@router.put("/projects/{project_id}")
def update_project(project_id: int, project_data: UpdateProjectRequest, db: Session = Depends(database.get_db)):
    logger.info(f"收到编辑项目信息请求: ID={project_id}")
    try:
        # 查找项目
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="项目未找到")

        # 更新项目信息
        if project_data.title is not None:
            project.title = project_data.title
        if project_data.summary is not None:
            project.summary = project_data.summary
        if project_data.date is not None:
            try:
                project.date = datetime.strptime(project_data.date, '%Y-%m-%d').date()
            except ValueError:
                logger.warning(f"日期格式错误: {project_data.date}")
        if project_data.status is not None:
            status_map = {'draft': 0, 'published': 1, 'recycled': 2}
            if project_data.status in status_map:
                project.status = status_map[project_data.status]

        # 处理标签更新
        if project_data.tags is not None:
            # 删除现有标签关联
            db.query(ProjectTag).filter(ProjectTag.project_id == project_id).delete()

            # 添加新标签
            for tag_name in project_data.tags:
                if not tag_name.strip():
                    continue

                tag = db.query(Tag).filter(Tag.name == tag_name.strip()).first()
                if not tag:
                    tag = Tag(name=tag_name.strip())
                    db.add(tag)
                    db.flush()

                # 创建项目-标签关联
                project_tag = ProjectTag(project_id=project.id, tag_id=tag.id)
                db.add(project_tag)

        # 更新文件内容
        if project_data.content is not None:
            try:
                save_project_file(project, project_data.content)
            except Exception as e:
                logger.warning(f"更新项目文件失败: {str(e)}")

        db.commit()

        logger.info(f"成功编辑项目信息: {project.title}")
        return {
            "message": "项目信息编辑成功",
            "id": project.id,
            "title": project.title
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"编辑项目信息时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"编辑项目信息时发生错误: {str(e)}")


# 编辑项目信息(POST方法，用于兼容性)
@router.post("/projects/{project_id}/edit")
def update_project_post(project_id: int, project_data: UpdateProjectRequest, db: Session = Depends(database.get_db)):
    return update_project(project_id, project_data, db)


# 删除项目，同时删除文件
@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"收到删除项目请求: ID={project_id}")
    try:
        # 查找项目
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="项目未找到")

        # 删除项目-标签关联
        db.query(ProjectTag).filter(ProjectTag.project_id == project_id).delete()

        # 删除markdown文件
        try:
            delete_project_file(project)
        except Exception as e:
            logger.warning(f"删除项目文件失败: {str(e)}")

        # 删除项目记录
        db.delete(project)
        db.commit()

        logger.info(f"成功删除项目: {project.title}")
        return {"message": "项目删除成功"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除项目时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除项目时发生错误: {str(e)}")


# ===== HELPER FUNCTIONS =====
# 生成安全的slug
def generate_safe_slug(text: str) -> str:
    if not text:
        return "untitled"

    # 转换为小写
    slug = text.lower().strip()
    # 保留中文、英文、数字，其他字符替换为连字符
    slug = re.sub(r'[^\w\u4e00-\u9fa5]+', '-', slug)
    # 去除连续的连字符
    slug = re.sub(r'-+', '-', slug)
    # 去除首尾连字符
    slug = slug.strip('-')

    return slug or "untitled"


# 保存项目文件到磁盘
def save_project_file(project: Project, content: str):
    try:
        # 项目文件保存到articles/projects目录
        base_paths = ["../frontend/dist/articles/projects", "../frontend/public/articles/projects"]

        for base_path in base_paths:
            os.makedirs(base_path, exist_ok=True)
            file_path = os.path.join(base_path, f"{project.slug}.md")

            # 构建文件内容
            file_content = content
            if not content.strip().startswith('#'):
                file_content = f"# {project.title}\n\n{content}"

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            logger.info(f"成功保存项目文件: {file_path}")

    except Exception as e:
        logger.error(f"保存项目文件失败: {str(e)}")
        raise


# 删除项目文件
def delete_project_file(project: Project):
    try:
        base_paths = ["../frontend/dist/articles/projects", "../frontend/public/articles/projects"]

        for base_path in base_paths:
            file_path = os.path.join(base_path, f"{project.slug}.md")
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"成功删除项目文件: {file_path}")
            else:
                logger.warning(f"项目文件不存在: {file_path}")

    except Exception as e:
        logger.error(f"删除项目文件失败: {str(e)}")
        raise
