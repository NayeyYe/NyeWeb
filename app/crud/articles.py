from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import database
from database import Article, Tag, ArticleTag
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("articles_api")

router = APIRouter()

@router.get("/articles")
def get_articles(db: Session = Depends(database.get_db)):
    """获取所有文章，按日期倒序排列"""
    logger.info("收到获取文章数据的请求")
    try:
        articles = db.query(Article).order_by(Article.date.desc()).all()
        logger.info(f"成功获取到 {len(articles)} 篇文章")

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

# 添加新的路由来处理带分类的文章请求
@router.get("/articles/{category:path}/{article_slug}")
def get_article_by_category_and_slug(category: str, article_slug: str, db: Session = Depends(database.get_db)):
    """根据分类和slug获取单篇文章详情"""
    logger.info(f"收到获取文章详情的请求，分类: {category}, slug: {article_slug}")
    try:
        # 构建完整的分类路径进行查找
        article = db.query(Article).filter(
            Article.category == category,
            Article.slug == article_slug
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
        article = db.query(Article).filter(Article.slug == article_slug).first()
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

@router.get("/tags")
def get_all_tags(db: Session = Depends(database.get_db)):
    """获取所有标签及其文章数量"""
    logger.info("收到获取���有标签的请求")
    try:
        # 移除有问题的查询，直接统计标签
        all_tags = []
        tag_counts = {}

        # 获取所有文章的标签统计
        articles = db.query(Article).all()
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
        articles = db.query(Article).all()
        logger.info(f"从数据库获取到 {len(articles)} 篇文章用于构建分类树")

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
