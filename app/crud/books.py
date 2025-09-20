import sys
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

sys.path.append("..")
import database
from database import Book, Tag, BookTag
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("books_api")

router = APIRouter()


# 添加请求模型
class CreateBookRequest(BaseModel):
    title: str
    description: Optional[str] = None
    cover: Optional[str] = "/avatar.jpg"  # 默认封面
    tags: Optional[List[str]] = []
    status: Optional[str] = 'draft'
    filename: str  # 现在存储网盘URL


# 添加编辑图书请求模型
class UpdateBookRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cover: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None


# 获取所有书籍（支持分页和筛选）
@router.get("/books")
def get_books(
    page: int = 1,
    limit: int = 6,
    search: str = None,
    tags: str = None,
    db: Session = Depends(database.get_db)
):
    logger.info(f"收到获取书籍数据的请求，页码: {page}, 每页数量: {limit}, 搜索: {search}, 标签: {tags}")
    try:
        # 构建基础查询
        query = db.query(Book).filter(Book.status == 1)
        
        # 应用搜索筛选
        if search:
            search = f"%{search}%"
            query = query.filter(
                (Book.title.ilike(search)) |
                (Book.description.ilike(search))
            )
        
        # 应用标签筛选 (AND 逻辑 - 必须包含所有选中的标签)
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            if tag_list:
                # 对每个标签进行单独的join和filter，实现AND筛选
                for tag_name in tag_list:
                    # 为每个标签创建一个子查询，确保书籍包含所有选中的标签
                    subquery = db.query(BookTag.book_id).join(Tag).filter(Tag.name == tag_name).subquery()
                    query = query.filter(Book.id.in_(subquery))
        
        # 获取总数量
        total_count = query.count()
        
        # 计算偏移量并获取分页数据
        offset = (page - 1) * limit
        books = query.offset(offset).limit(limit).all()
        
        logger.info(f"成功获取到 {len(books)} 本已发布书籍")

        # 转换为前端需要的格式
        books_data = []
        for book in books:
            # 获取书籍的标签
            book_tags = db.query(Tag).join(BookTag).filter(BookTag.book_id == book.id).all()
            tags = [tag.name for tag in book_tags]

            book_dict = {
                "id": book.id,
                "title": book.title,
                "description": book.description,
                "cover": book.cover if book.cover and book.cover.startswith(
                    'http') else "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg",  # 使用图床URL
                "filename": book.filename,
                "tags": tags
            }
            books_data.append(book_dict)

        # 返回分页数据
        return {
            "data": books_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "pages": (total_count + limit - 1) // limit if limit > 0 else 0  # 计算总页数
            }
        }
    except Exception as e:
        logger.error(f"获取书籍数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取书籍数据时发生错误: {str(e)}")


# 根据ID获取单本书籍详情
@router.get("/books/{book_id}")
def get_book_by_id(book_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"收到获取书籍详情的请求，ID: {book_id}")
    try:
        book = db.query(Book).filter(Book.id == book_id, Book.status == 1).first()
        if not book:
            logger.warning(f"未找到书籍，ID: {book_id}")
            raise HTTPException(status_code=404, detail="书籍未找到")

        # 获取书籍的标签
        book_tags = db.query(Tag).join(BookTag).filter(BookTag.book_id == book.id).all()
        tags = [tag.name for tag in book_tags]

        book_dict = {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "cover": book.cover if book.cover and book.cover.startswith(
                'http') else "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg",  # 使用图床URL
            "filename": book.filename,
            "tags": tags
        }

        logger.info(f"成功获取书籍详情: {book.title}")
        return book_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取书籍详情时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取书籍详情时发生错误: {str(e)}")


# 获取所有书籍标签及其书籍数量
@router.get("/book-tags")
def get_all_book_tags(db: Session = Depends(database.get_db)):
    logger.info("收到获取所有书籍标签的请求")
    try:
        all_tags = []
        tag_counts = {}

        # 获取所有已发布书籍的标签统计
        books = db.query(Book).filter(Book.status == 1).all()
        for book in books:
            book_tags = db.query(Tag).join(BookTag).filter(BookTag.book_id == book.id).all()
            for tag in book_tags:
                if tag.name not in all_tags:
                    all_tags.append(tag.name)
                tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1

        logger.info(f"成功获取 {len(all_tags)} 个书籍标签")
        return {
            "tags": all_tags,
            "counts": tag_counts
        }
    except Exception as e:
        logger.error(f"获取书籍标签时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取书籍标签时发生错误: {str(e)}")


# 管理员获取所有书籍(包含所有状态)
@router.get("/admin/books")
def get_all_books_admin(db: Session = Depends(database.get_db)):
    logger.info("收到管理员获取全部书籍数据的请求")
    try:
        books = db.query(Book).all()
        logger.info(f"成功获取到 {len(books)} 本书籍（所有状态）")

        # 转换为前端需要的格式
        books_data = []
        for book in books:
            # 获取书籍的标签
            book_tags = db.query(Tag).join(BookTag).filter(BookTag.book_id == book.id).all()
            tags = [tag.name for tag in book_tags]

            # 状态映射
            status_map = {0: 'draft', 1: 'published', 2: 'recycled'}

            book_dict = {
                "id": book.id,
                "title": book.title,
                "description": book.description,
                "cover": book.cover if book.cover and book.cover.startswith(
                    'http') else "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg",  # 使用图床URL
                "filename": book.filename,
                "tags": tags,
                "status": status_map.get(book.status, 'draft')
            }
            books_data.append(book_dict)
            logger.info(f"书籍数据: ID={book.id}, 标题={book.title}, 状态={book.status}")

        return books_data
    except Exception as e:
        logger.error(f"获取书籍数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取书籍数据时发生错误: {str(e)}")


# 修改书籍状态
@router.patch("/books/{book_id}/status")
def update_book_status(book_id: int, status_data: dict, db: Session = Depends(database.get_db)):
    logger.info(f"收到修改书籍状态请求: ID={book_id}, 状态={status_data.get('status')}")
    try:
        # 查找书籍
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="书籍未找到")

        # 状态映射
        status_map = {'draft': 0, 'published': 1, 'recycled': 2}
        new_status = status_data.get('status')

        if new_status not in status_map:
            raise HTTPException(status_code=400, detail="无效的状态值")

        # 更新状态
        old_status = book.status
        book.status = status_map[new_status]
        db.commit()

        logger.info(f"成功修改书籍状态: {book.title}, {old_status} -> {book.status}")
        return {"message": "书籍状态修改成功", "status": new_status}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"修改书籍状态时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"修改书籍状态时发生错误: {str(e)}")


# 删除书籍
@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"收到删除书籍请求: ID={book_id}")
    try:
        # 查找书籍
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="书籍未找到")

        # 删除书籍-标签关联
        db.query(BookTag).filter(BookTag.book_id == book_id).delete()

        # 删除书籍记录
        db.delete(book)
        db.commit()

        logger.info(f"成功删除书籍: {book.title}")
        return {"message": "书籍删除成功"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除书籍时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除书籍时发生错误: {str(e)}")


# 创建新图书
@router.post("/admin/books")
def create_book(book_data: CreateBookRequest, db: Session = Depends(database.get_db)):
    logger.info(f"收到创建图书请求: {book_data.title}")
    try:
        # 状态映射
        status_map = {'draft': 0, 'published': 1, 'recycled': 2}
        status = status_map.get(book_data.status, 0)

        # 处理封面URL，确保是有效的图床链接
        cover_url = book_data.cover
        if not cover_url or cover_url == "/avatar.jpg":
            cover_url = "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg"

        # 验证URL格式
        import re
        url_pattern = r'^https?://.+\.(jpg|jpeg|png|gif|webp)(\?.*)?$'
        if not re.match(url_pattern, cover_url, re.IGNORECASE):
            logger.warning(f"封面URL格式不正确，使用默认封面: {cover_url}")
            cover_url = "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg"

        # 验证网盘URL格式
        if not book_data.filename.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="网盘链接必须以http://或https://开头")

        # 创建图书记录
        new_book = Book(
            title=book_data.title,
            description=book_data.description,
            cover=cover_url,
            filename=book_data.filename,  # 现在存储网盘URL
            status=status
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        # 处理标签
        for tag_name in book_data.tags or []:
            if not tag_name.strip():
                continue

            tag = db.query(Tag).filter(Tag.name == tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
                db.add(tag)
                db.flush()

            # 创建图书-标签关联
            book_tag = BookTag(book_id=new_book.id, tag_id=tag.id)
            db.add(book_tag)

        db.commit()

        logger.info(f"成功创建图书: {new_book.title}, 网盘链接: {book_data.filename}")
        return {
            "message": "图书创建成功",
            "id": new_book.id,
            "filename": new_book.filename
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建图书时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建图书时发生错误: {str(e)}")


# 编辑图书信息
@router.put("/admin/books/{book_id}")
def update_book(book_id: int, book_data: UpdateBookRequest, db: Session = Depends(database.get_db)):
    logger.info(f"收到编辑图书信息请求: ID={book_id}")
    try:
        # 查找书籍
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="书籍未找到")

        # 更新图书信息
        if book_data.title is not None:
            book.title = book_data.title
        if book_data.description is not None:
            book.description = book_data.description
        if book_data.cover is not None:
            # 处理封面URL，验证格式
            cover_url = book_data.cover
            if cover_url == "/avatar.jpg":
                cover_url = "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg"
            else:
                # 验证URL格式
                import re
                url_pattern = r'^https?://.+\.(jpg|jpeg|png|gif|webp)(\?.*)?$'
                if not re.match(url_pattern, cover_url, re.IGNORECASE):
                    logger.warning(f"封面URL格式不正确，使用默认封面: {cover_url}")
                    cover_url = "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg"

            book.cover = cover_url
        if book_data.status is not None:
            status_map = {'draft': 0, 'published': 1, 'recycled': 2}
            if book_data.status in status_map:
                book.status = status_map[book_data.status]

        # 处理标签更新
        if book_data.tags is not None:
            # 删除现有标签关联
            db.query(BookTag).filter(BookTag.book_id == book_id).delete()

            # 添加新标签
            for tag_name in book_data.tags:
                if not tag_name.strip():
                    continue

                tag = db.query(Tag).filter(Tag.name == tag_name.strip()).first()
                if not tag:
                    tag = Tag(name=tag_name.strip())
                    db.add(tag)
                    db.flush()

                # 创建图书-标签关联
                book_tag = BookTag(book_id=book.id, tag_id=tag.id)
                db.add(book_tag)

        db.commit()

        logger.info(f"成功编辑图书信息: {book.title}")
        return {
            "message": "图书信息编辑成功",
            "id": book.id,
            "title": book.title
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"编辑图书信息时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"编辑图书信息时发生错误: {str(e)}")
        if book_data.description is not None:
            book.description = book_data.description
        if book_data.cover is not None:
            # 处理封面URL，验证格式
            cover_url = book_data.cover
            if cover_url == "/avatar.jpg":
                cover_url = "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg"
            else:
                # 验证URL格式
                import re
                url_pattern = r'^https?://.+\.(jpg|jpeg|png|gif|webp)(\?.*)?$'
                if not re.match(url_pattern, cover_url, re.IGNORECASE):
                    logger.warning(f"封面URL格式不正确，使用默认封面: {cover_url}")
                    cover_url = "https://ooo.0x0.ooo/2025/09/18/OlGAw6.jpg"

            book.cover = cover_url
        if book_data.status is not None:
            status_map = {'draft': 0, 'published': 1, 'recycled': 2}
            if book_data.status in status_map:
                book.status = status_map[book_data.status]

        # 处理标签更新
        if book_data.tags is not None:
            # 删除现有标签关联
            db.query(BookTag).filter(BookTag.book_id == book_id).delete()

            # 添加新标签
            for tag_name in book_data.tags:
                if not tag_name.strip():
                    continue

                tag = db.query(Tag).filter(Tag.name == tag_name.strip()).first()
                if not tag:
                    tag = Tag(name=tag_name.strip())
                    db.add(tag)
                    db.flush()

                # 创建图书-标签关联
                book_tag = BookTag(book_id=book.id, tag_id=tag.id)
                db.add(book_tag)

        db.commit()

        logger.info(f"成功编辑图书信息: {book.title}")
        return {
            "message": "图书信息编辑成功",
            "id": book.id,
            "title": book.title
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"编辑图书信息时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"编辑图书信息时发生错误: {str(e)}")
