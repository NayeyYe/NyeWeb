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
import re

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("articles_api")

router = APIRouter()

# ===== REQUEST MODELS =====
class CreateArticleRequest(BaseModel):
    title: str
    slug: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    status: Optional[str] = 'draft'
    content: str
    date: Optional[str] = None

class GenerateSummaryRequest(BaseModel):
    content: str
    title: Optional[str] = None

class CreateCategoryRequest(BaseModel):
    name: str
    path: Optional[str] = None
    parent: Optional[str] = None

# ===== CATEGORY MANAGEMENT APIs =====
@router.get("/articles/categories")
def get_article_categories():
    """获取所有文章分类树结构（基于物理文件夹）"""
    logger.info("收到获取文章分类树的请求")
    try:
        # 扫描物理文件夹获取所有分类
        physical_categories = scan_physical_categories()
        logger.info(f"扫描到物理分类: {[cat['path'] for cat in physical_categories]}")

        # 构建分类树数据
        categories_data = []

        for cat in physical_categories:
            if cat["path"]:  # 确保路径不为空
                categories_data.append({
                    "path": cat["path"],
                    "count": cat["count"],
                    "articles": cat.get("articles", [])
                })

        # 如果没有分类，创建一个默认提示
        if len(categories_data) == 0:
            categories_data = [{
                "path": "请先创建分类文件夹",
                "count": 0,
                "articles": []
            }]

        logger.info(f"成功构建分类树，包含 {len(categories_data)} 个分类")
        return {
            "categories": categories_data,
            "total": len(categories_data)
        }
    except Exception as e:
        logger.error(f"获取文章分类树时发生错误: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        # 即使出错，也返回一个默认分类，避免前端报错
        return {
            "categories": [{
                "path": "error",
                "count": 0,
                "articles": []
            }],
            "total": 1
        }

@router.post("/articles/categories")
def create_category(request: CreateCategoryRequest, db: Session = Depends(database.get_db)):
    """创建新的文章分类文件夹"""
    logger.info(f"收到创建分类文件夹请求: {request.name}")
    try:
        # 生成分类路径
        if not request.path:
            # 清理文件夹名称，确保安全
            safe_name = request.name.strip()
            # 移除特殊字符，保留中文、英文、数字、下划线和连字符
            safe_name = re.sub(r'[^\w\u4e00-\u9fa5\-]', '-', safe_name)
            safe_name = re.sub(r'-+', '-', safe_name).strip('-')

            if request.parent:
                path = f"{request.parent}/{safe_name}"
            else:
                path = safe_name
        else:
            path = request.path

        # 检查路径是否为空
        if not path:
            raise HTTPException(status_code=400, detail="分类路径不能为空")

        # 检查物理文件夹是否已存在
        base_path = "../frontend/dist/articles/knowledge"
        full_path = os.path.join(base_path, path.replace('/', os.sep))

        if os.path.exists(full_path):
            raise HTTPException(status_code=409, detail="分类文件夹已存在")

        # 创建物理文件夹
        try:
            create_physical_category_folder(path)
        except Exception as e:
            logger.error(f"创建物理文件夹失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"创建文件夹失败: {str(e)}")

        logger.info(f"成功创建分类文件夹: {request.name} -> {path}")
        return {
            "message": "分类文件夹创建成功",
            "name": request.name,
            "path": path
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建分类文件夹时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建分类文件夹时发生错误: {str(e)}")

# ===== ARTICLE QUERY APIs =====
@router.get("/articles")
def get_articles(db: Session = Depends(database.get_db)):
    """获取所有已发布文章，按日期倒序排列"""
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

        return articles_data
    except Exception as e:
        logger.error(f"获取文章数据时��生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文章数据时发生错误: {str(e)}")

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

        return articles_data
    except Exception as e:
        logger.error(f"获取文章数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文章数据时发生错误: {str(e)}")

@router.get("/articles/{category:path}/{article_slug}")
def get_article_by_category_and_slug(category: str, article_slug: str, db: Session = Depends(database.get_db)):
    """根据分类和slug获取单篇文章详情"""
    logger.info(f"收到获取文章详情的请求，分类: {category}, slug: {article_slug}")
    try:
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

# ===== ARTICLE MANAGEMENT APIs =====
@router.post("/articles")
def create_article(article_data: CreateArticleRequest, db: Session = Depends(database.get_db)):
    """创建新文章"""
    logger.info(f"收到创建文章请求: {article_data.title}")
    try:
        # 生成或验证slug，自动从标题生成
        if not article_data.slug:
            slug = generate_safe_slug(article_data.title)
        else:
            slug = generate_safe_slug(article_data.slug)
        
        # 确保slug唯一性
        base_slug = slug
        counter = 1
        while db.query(Article).filter(Article.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # 解析日期
        article_date = datetime.now().date()
        if article_data.date:
            try:
                article_date = datetime.strptime(article_data.date, '%Y-%m-%d').date()
            except ValueError:
                logger.warning(f"日期格式错误，使用当前日期: {article_data.date}")
        
        # 状态映射
        status_map = {'draft': 0, 'published': 1, 'recycled': 2}
        status = status_map.get(article_data.status, 0)
        
        # 创建文章记录
        new_article = Article(
            title=article_data.title,
            slug=slug,
            summary=article_data.summary,
            category=article_data.category,
            date=article_date,
            status=status
        )
        
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        
        # 处理标签
        for tag_name in article_data.tags or []:
            if not tag_name.strip():
                continue
                
            tag = db.query(Tag).filter(Tag.name == tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
                db.add(tag)
                db.flush()
            
            # 创建文章-标签关联
            article_tag = ArticleTag(article_id=new_article.id, tag_id=tag.id)
            db.add(article_tag)
        
        db.commit()
        
        # 创建markdown文件，确保分类文件夹存在
        try:
            save_article_file(new_article, article_data.content, article_data.category)
        except Exception as e:
            logger.warning(f"保存文章文件失败: {str(e)}")
        
        logger.info(f"成功创建文章: {new_article.title}")
        return {
            "message": "文章上传成功", 
            "id": new_article.id,
            "slug": new_article.slug
        }
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建文章时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建文章时发生错误: {str(e)}")

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

@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(database.get_db)):
    """删除文章，同时删除dist和public中的文件"""
    logger.info(f"收到删除文章请求: ID={article_id}")
    try:
        # 查找文章
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="文章未找到")
        
        # 删除文章-标签关联
        db.query(ArticleTag).filter(ArticleTag.article_id == article_id).delete()
        
        # 删除markdown文件（dist和public）
        for base_path in ["../frontend/dist/articles/knowledge", "../frontend/public/articles/knowledge"]:
            try:
                file_path = base_path
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

# ===== AI & UTILITY APIs =====
@router.post("/articles/generate-summary")
async def generate_summary(request: GenerateSummaryRequest):
    """使用AI生成文章摘要"""
    logger.info(f"收到生成摘要请求，标题: {request.title}")
    try:
        # 这里可以集成各种大模型API
        summary = await call_ai_api_for_summary(request.content, request.title)

        if summary:
            logger.info("摘要生成成功")
            return {"summary": summary}
        else:
            # 降级方案：简单文本提取
            fallback_summary = extract_simple_summary(request.content)
            return {"summary": fallback_summary}

    except Exception as e:
        logger.error(f"生成摘要时发生错误: {str(e)}")
        # 返回降级方案而不是抛出异常
        fallback_summary = extract_simple_summary(request.content)
        return {"summary": fallback_summary}

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
        # 即使出错，也返回空数据，避免前端报错
        return {
            "tags": [],
            "counts": {}
        }

# ===== HELPER FUNCTIONS =====
def scan_physical_categories():
    """扫描物理文件夹获取分类（完全基于文件系统）"""
    categories = []
    base_path = "../frontend/dist/articles/knowledge"

    try:
        # 获取绝对路径
        abs_base_path = os.path.abspath(base_path)
        logger.info(f"扫描物理文件夹路径: {abs_base_path}")

        # 确保基础路径存在
        os.makedirs(abs_base_path, exist_ok=True)

        if os.path.exists(abs_base_path):
            # 递归遍历所有子目录
            for root, dirs, files in os.walk(abs_base_path):
                # 过滤掉隐藏文件夹、系统文件夹和assets文件夹
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'assets']

                # 计算相对路径
                rel_path = os.path.relpath(root, abs_base_path)

                # 跳过根目录本身
                if rel_path == '.':
                    continue

                # 转换路径分隔符为统一的斜杠
                category_path = rel_path.replace(os.sep, '/')

                # 过滤掉以.开头的隐藏文件夹路径和assets路径
                path_parts = category_path.split('/')
                if any(part.startswith('.') or part == 'assets' for part in path_parts):
                    continue

                # 统计markdown文件数量（排除README.md和其他特殊文件）
                md_files = [f for f in files
                          if f.endswith('.md')
                          and f not in ['README.md', '.gitkeep', 'index.md']
                          and not f.startswith('.')]
                md_count = len(md_files)

                logger.info(f"发现分类文件夹: {category_path}, markdown文件: {md_files}")

                categories.append({
                    "path": category_path,
                    "count": md_count,
                    "articles": md_files
                })

        logger.info(f"扫描物理文件夹完成，找到 {len(categories)} 个分类")

        # 打印所有发现的分类路径用于调试
        for cat in categories:
            logger.info(f"  - {cat['path']} ({cat['count']} 文件)")

    except Exception as e:
        logger.error(f"扫描物理分类文件夹失败: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")

    return categories

def create_physical_category_folder(category_path: str):
    """创建物理分类文件夹"""
    try:
        # 构建完整的文件系统路径
        for base_path in ["../frontend/dist/articles/knowledge", "../frontend/public/articles/knowledge"]:
            full_path = os.path.join(base_path, category_path.replace('/', os.sep))
            
            # 创建目录
            os.makedirs(full_path, exist_ok=True)

            # 创建README.md文件说明该分类
            readme_path = os.path.join(full_path, 'README.md')
            if not os.path.exists(readme_path):
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {category_path.split('/')[-1]}\n\n")
                    f.write(f"分类路径: {category_path}\n\n")
                    f.write("此文件夹用于存储相关文章。\n")

            logger.info(f"成功创建物理文件夹: {full_path}")

    except Exception as e:
        logger.error(f"创建物理文件夹失败: {str(e)}")
        raise

# ...existing AI helper functions...
async def call_ai_api_for_summary(content: str, title: str = None) -> str:
    """调用AI API生成摘要"""
    try:
        # 这里可以调用不同的AI服务
        # 例如：OpenAI GPT, 百度千帆, 阿里云通义千问等

        # 示例：调用OpenAI API
        # import openai
        # response = await openai.ChatCompletion.acreate(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "你是一个专业的文章摘要生成助手。请为以下文章生成一个简洁、准确的摘要，长度控制在100-200字之间。"},
        #         {"role": "user", "content": f"标题：{title}\n\n内容：{content[:2000]}"}
        #     ],
        #     max_tokens=300
        # )
        # return response.choices[0].message.content.strip()

        # ��例：模拟AI响应
        import asyncio
        await asyncio.sleep(1)  # 模拟API调用延迟

        # 简单的文本处理作为示例
        summary = extract_simple_summary(content)
        return summary

    except Exception as e:
        logger.error(f"调用AI API失败: {str(e)}")
        return None

def extract_simple_summary(content: str) -> str:
    """简单的摘要提取降级方案"""
    if not content:
        return ""

    # 移除markdown标记
    import re
    text = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)  # 移除标题
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # 移除粗体
    text = re.sub(r'\*(.*?)\*', r'\1', text)  # 移除斜体
    text = re.sub(r'`(.*?)`', r'\1', text)  # 移除行内代码
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # 移除链接
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # 移除图片
    text = re.sub(r'```[\s\S]*?```', '', text)  # 移除代码块
    text = re.sub(r'\n{2,}', '\n', text)  # 移除多余换行
    text = text.strip()

    # 取前150字符作为摘要
    if len(text) > 150:
        text = text[:150] + "..."

    return text

def generate_safe_slug(text: str) -> str:
    """生成安全的slug"""
    if not text:
        return "untitled"

    import re
    # 转换为小写
    slug = text.lower().strip()
    # 保留中文、英文、数字，其他字符替换为连字符
    slug = re.sub(r'[^\w\u4e00-\u9fa5]+', '-', slug)
    # 去除连续的连字符
    slug = re.sub(r'-+', '-', slug)
    # 去除首尾连字符
    slug = slug.strip('-')

    return slug or "untitled"

def save_article_file(article: Article, content: str, category: str = None):
    """保存文章文件到磁盘，确保分类文件夹存在（dist和public）"""
    try:
        # 构建文件路径
        dist_base_path = "../frontend/dist/articles/knowledge"
        public_base_path = "../frontend/public/articles/knowledge"
        paths = []
        for base_path in [dist_base_path, public_base_path]:
            if category:
                file_path = os.path.join(base_path, category.replace('/', os.sep))
            else:
                file_path = base_path
            os.makedirs(file_path, exist_ok=True)
            file_full_path = os.path.join(file_path, f"{article.slug}.md")
            paths.append(file_full_path)

        # 构建文件内容
        file_content = content
        if not content.strip().startswith('#'):
            file_content = f"# {article.title}\n\n{content}"

        # 保存到两个位置
        for file_full_path in paths:
            with open(file_full_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            logger.info(f"成功保存文章文件: {file_full_path}")

    except Exception as e:
        logger.error(f"保存文章文件失败: {str(e)}")
        raise
        raise
