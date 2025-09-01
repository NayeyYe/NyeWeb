from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import database
from database import Book, Tag, BookTag
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("books_api")

router = APIRouter()

@router.get("/books")
def get_books(db: Session = Depends(database.get_db)):
    """获取所有书籍"""
    logger.info("收到获取书籍数据的请求")
    try:
        books = db.query(Book).all()
        logger.info(f"成功获取到 {len(books)} 本书籍")

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
                "cover": book.cover,
                "filename": book.filename,
                "tags": tags
            }
            books_data.append(book_dict)
            logger.info(f"书籍数据: ID={book.id}, 标题={book.title}")

        return books_data
    except Exception as e:
        logger.error(f"获取书籍数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取书籍数据时发生错误: {str(e)}")

@router.get("/books/{book_id}")
def get_book_by_id(book_id: int, db: Session = Depends(database.get_db)):
    """根据ID获取单本书籍详情"""
    logger.info(f"收到获取书籍详情的请求，ID: {book_id}")
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
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
            "cover": book.cover,
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

@router.get("/book-tags")
def get_all_book_tags(db: Session = Depends(database.get_db)):
    """获取所有书籍标签及其书籍数量"""
    logger.info("收到获取所有书籍标签的请求")
    try:
        all_tags = []
        tag_counts = {}

        # 获取所有书籍的标签统计
        books = db.query(Book).all()
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

