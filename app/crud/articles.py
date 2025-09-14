import sys

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.append("..")
import database
from database import Article, Tag, ArticleTag
import logging
from pydantic import BaseModel
from typing import Optional, List
import os
from datetime import datetime

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("articles_api")

router = APIRouter()

# 添加请求模型
class CreateArticleRequest(BaseModel):
    title: str
    summary: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []

@router.get("/articles")
def get_articles(db: Session = Depends(database.get_db)):
    """获取所有文章，按日期倒序排列"""
    logger.info("收到获取文章数据的请求")
    try:
        articles = db.query(Article).filter(Article.status == 1).order_by(Article.date.desc()).all()
        logger.info(f"成功获取到 {len(articles)} 篇已发布文章")

        # 转换为前端需要的格式
        articles_data = []
        for article in articles:
            # 获取文章的标签
            article_tags = db.query(Tag).join(ArticleTag).filter(ArticleTag.article_id == article.id).all()
            tags = [tag.name for tag in article_tags]

            article_dict = {
                "id": article.id,
                "title": article.title,
                "slug": article.slug,
                "summary": article.summary,
                "category": article.category,
                "date": article.date.strftime('%Y-%m-%d') if article.date else None,
                "tags": tags
            }
            articles_data.append(article_dict)
            logger.info(f"文章数据: ID={article.id}, 标题={article.title}, 分类={article.category}, slug={article.slug}")

        return articles_data
    except Exception as e:
        logger.error(f"获取文章数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文章数据时发生错误: {str(e)}")

# 新增管理员获取全部文章的接口
@router.get("/admin/articles")
def get_all_articles_admin(db: Session = Depends(database.get_db)):
    """管理员获取所有文章（包含所有状态），按日期倒序排列"""
    logger.info("收到管理员获取全部文章数据的请求")
    try:
        articles = db.query(Article).order_by(Article.date.desc()).all()
        logger.info(f"成功获取到 {len(articles)} 篇文章（所有状态）")

        # 转换为前端需要的格式
        articles_data = []
        for article in articles:
            # 获取文章的标签
            article_tags = db.query(Tag).join(ArticleTag).filter(ArticleTag.article_id == article.id).all()
            tags = [tag.name for tag in article_tags]

            # 状态映射
            status_map = {0: 'draft', 1: 'published', 2: 'recycled'}
            
            article_dict = {
                "id": article.id,
                "title": article.title,
                "slug": article.slug,
                "summary": article.summary,
                "category": article.category,
                "date": article.date.strftime('%Y-%m-%d') if article.date else None,
                "tags": tags,
                "status": status_map.get(article.status, 'draft')
            }
            articles_data.append(article_dict)
            logger.info(f"文章数据: ID={article.id}, 标题={article.title}, 状态={article.status}")

        return articles_data
    except Exception as e:
        logger.error(f"获取文章数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文章数据时发生错误: {str(e)}")

# 新增修改文章状态的接口
@router.patch("/articles/{article_id}/status")
def update_article_status(article_id: int, status_data: dict, db: Session = Depends(database.get_db)):
    """修改文章状态"""
    logger.info(f"收到修改文章状态请求: ID={article_id}, 状态={status_data.get('status')}")
    try:
        # 查找文章
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="文章未找到")
        
        # 状态映射
        status_map = {'draft': 0, 'published': 1, 'recycled': 2}
        new_status = status_data.get('status')
        
        if new_status not in status_map:
            raise HTTPException(status_code=400, detail="无效的状态值")
        
        # 更新状态
        old_status = article.status
        article.status = status_map[new_status]
        db.commit()
        
        logger.info(f"成功修改文章状态: {article.title}, {old_status} -> {article.status}")
        return {"message": "文章状态修改成功", "status": new_status}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"修改文章状态时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"修改文章状态时发生错误: {str(e)}")

@router.get("/articles/{category:path}/{article_slug}")
def get_article_by_category_and_slug(category: str, article_slug: str, db: Session = Depends(database.get_db)):
    """根据分类和slug获取单篇文章详情"""
    logger.info(f"收到获取文章详情的请求，分类: {category}, slug: {article_slug}")
    try:
        # 构建完整的分类路径进行查找
        article = db.query(Article).filter(
            Article.category == category,
            Article.slug == article_slug,
            Article.status == 1
        ).first()

        if not article:
            logger.warning(f"未找到文章，分类: {category}, slug: {article_slug}")
            raise HTTPException(status_code=404, detail="文章未找到")

        # 获取文章的标签
        article_tags = db.query(Tag).join(ArticleTag).filter(ArticleTag.article_id == article.id).all()
        tags = [tag.name for tag in article_tags]

        article_dict = {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "summary": article.summary,
            "category": article.category,
            "date": article.date.strftime('%Y-%m-%d') if article.date else None,
            "tags": tags
        }

        logger.info(f"成功获取文章详情: {article.title}")
        return article_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取文章详情时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文章详情时发生错误: {str(e)}")

@router.get("/articles/{article_slug}")
def get_article_by_slug(article_slug: str, db: Session = Depends(database.get_db)):
    """根据slug获取单篇文章详情"""
    logger.info(f"收到获取文章详情的请求，slug: {article_slug}")
    try:
        article = db.query(Article).filter(Article.slug == article_slug, Article.status == 1).first()
        if not article:
            logger.warning(f"未找到文章，slug: {article_slug}")
            raise HTTPException(status_code=404, detail="文章未找到")

        # 获取文章的标签
        article_tags = db.query(Tag).join(ArticleTag).filter(ArticleTag.article_id == article.id).all()
        tags = [tag.name for tag in article_tags]

        article_dict = {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "summary": article.summary,
            "category": article.category,
            "date": article.date.strftime('%Y-%m-%d') if article.date else None,
            "tags": tags
        }

        logger.info(f"成功获取文章详情: {article.title}")
        return article_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取文章详情时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文章详情时发生错误: {str(e)}")

@router.post("/articles")
def create_article(article_data: CreateArticleRequest, db: Session = Depends(database.get_db)):
    """创建新文章"""
    logger.info(f"收到创建文章请求: {article_data.title}")
    try:
        # 生成slug
        slug = article_data.title.lower().replace(' ', '-').replace('/', '-')
        
        # 检查slug是否已存在
        existing_article = db.query(Article).filter(Article.slug == slug).first()
        if existing_article:
            raise HTTPException(status_code=400, detail="文章标题已存在，请修改标题")
        
        # 创建文章记录
        new_article = Article(
            title=article_data.title,
            slug=slug,
            summary=article_data.summary,
            category=article_data.category,
            date=datetime.now().date()
        )
        
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        
        # 处理标签
        for tag_name in article_data.tags or []:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            
            # 创建文章-标签关联
            article_tag = ArticleTag(article_id=new_article.id, tag_id=tag.id)
            db.add(article_tag)
        
        db.commit()
        
        # 创建markdown文件
        try:
            file_path = f"frontend/dist/articles/knowledge"
            if article_data.category:
                file_path += f"/{article_data.category}"
            
            os.makedirs(file_path, exist_ok=True)
            
            markdown_content = f"# {article_data.title}\n\n"
            if article_data.summary:
                markdown_content += f"{article_data.summary}\n\n"
            markdown_content += "<!-- 请在此处添加文章内容 -->\n"
            
            with open(f"{file_path}/{slug}.md", 'w', encoding='utf-8') as f:
                f.write(markdown_content)
                
            logger.info(f"成功创建markdown文件: {file_path}/{slug}.md")
        except Exception as e:
            logger.warning(f"创建markdown文件失败: {str(e)}")
        
        logger.info(f"成功创建文章: {new_article.title}")
        return {"message": "文章创建成功", "id": new_article.id}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建文章时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建文章时发生错误: {str(e)}")

@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(database.get_db)):
    """删除文章"""
    logger.info(f"收到删除文章请求: ID={article_id}")
    try:
        # 查找文章
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="文章未找到")
        
        # 删除文章-标签关联
        db.query(ArticleTag).filter(ArticleTag.article_id == article_id).delete()
        
        # 删除markdown文件
        try:
            file_path = f"frontend/dist/articles/knowledge"
            if article.category:
                file_path += f"/{article.category}"
            file_path += f"/{article.slug}.md"
            
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"成功删除markdown文件: {file_path}")
            else:
                logger.warning(f"markdown文件不存在: {file_path}")
                
        except Exception as e:
            logger.warning(f"删除markdown文件失败: {str(e)}")
        
        # 删除文章记录
        db.delete(article)
        db.commit()
        
        logger.info(f"成功删除文章: {article.title}")
        return {"message": "文章删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除文章时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除文章时发生错误: {str(e)}")

@router.get("/tags")
def get_all_tags(db: Session = Depends(database.get_db)):
    """获取所有标签及其文章数量"""
    logger.info("收到获取所有标签的请求")
    try:
        all_tags = []
        tag_counts = {}

        # 获取所有已发布文章的标签统计
        articles = db.query(Article).filter(Article.status == 1).all()
        for article in articles:
            article_tags = db.query(Tag).join(ArticleTag).filter(ArticleTag.article_id == article.id).all()
            for tag in article_tags:
                if tag.name not in all_tags:
                    all_tags.append(tag.name)
                tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1

        logger.info(f"成功获取 {len(all_tags)} 个标签")
        return {
            "tags": all_tags,
            "counts": tag_counts
        }
    except Exception as e:
        logger.error(f"获取标签时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取标签时发生错误: {str(e)}")

@router.get("/articles/categories")
def get_article_categories(db: Session = Depends(database.get_db)):
    """获取所有文章分类树结构"""
    logger.info("收到获取文章分类树的请求")
    try:
        articles = db.query(Article).filter(Article.status == 1).all()
        logger.info(f"从数据库获取到 {len(articles)} 篇已发布文章用于构建分类树")

        # 构建分类树数据
        categories = {}
        for article in articles:
            if not article.category:
                continue

            category_path = article.category
            if category_path not in categories:
                categories[category_path] = {
                    "path": category_path,
                    "count": 0,
                    "articles": []
                }
            categories[category_path]["count"] += 1
            categories[category_path]["articles"].append({
                "id": article.id,
                "title": article.title,
                "slug": article.slug
            })

        # 转换为树形结构数据
        tree_data = []
        for category_path, category_info in categories.items():
            tree_data.append({
                "path": category_path,
                "count": category_info["count"],
                "articles": category_info["articles"]
            })

        logger.info(f"成功构建分类树，包含 {len(tree_data)} 个分类")
        return {
            "categories": tree_data,
            "total": len(categories)
        }
    except Exception as e:
        logger.error(f"获取文章分类树时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文章分类树时发生错误: {str(e)}")
