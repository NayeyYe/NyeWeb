import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 加载环境变量
load_dotenv()

# 获取数据库URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=False)

# 创建SessionLocal类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类
Base = declarative_base()

# 时间线模型
class Timeline(Base):
    __tablename__ = "timeline"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)

# 文章模型
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    category = Column(String(100))
    date = Column(Date)
    summary = Column(Text)

# 标签模型
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

# 文章标签关联模型
class ArticleTag(Base):
    __tablename__ = "article_tags"

    article_id = Column(Integer, ForeignKey('articles.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

# 项目模型
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    date = Column(Date)
    summary = Column(Text)

# 项目标签关联模型
class ProjectTag(Base):
    __tablename__ = "project_tags"

    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

# 书籍模型
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    cover = Column(String(500))  # 封面图片路径
    filename = Column(String(255))  # PDF文件名

# 书籍标签关联模型
class BookTag(Base):
    __tablename__ = "book_tags"

    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

# ���表模型
class Figure(Base):
    __tablename__ = "figures"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    filename = Column(String(255))  # 图片文件名

# 图表标签关联模型
class FigureTag(Base):
    __tablename__ = "figure_tags"

    figure_id = Column(Integer, ForeignKey('figures.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

# 收藏图片模型
class FavoriteImage(Base):
    __tablename__ = "favorite_images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)

# 工具模型
class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    url = Column(String(2083))  # URL字段

# 工具标签关联模型
class ToolTag(Base):
    __tablename__ = "tool_tags"

    tool_id = Column(Integer, ForeignKey('tools.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)


# Admin模型定义
class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)


# 数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
