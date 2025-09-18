# 数据库初始化脚本
# 用于创建表和插入初始数据
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crud.admin import create_admin
from database import Admin
from database import Base

# 加载环境变量
load_dotenv()


# 创建数据库表
def create_database_tables(engine):
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功!")


def create_admin_account(db):
    """创建管理员账户"""
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    if not ADMIN_PASSWORD:
        raise ValueError("ADMIN_PASSWORD environment variable is not set")

    # 检查是否已存在管理员
    existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
    if not existing_admin:
        create_admin(db, "admin", ADMIN_PASSWORD)
        print("管理员账户创建成功!")
    else:
        print("管理员账户已存在!")


# 初始化数据库表
def init_database():
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")

    engine = create_engine(DATABASE_URL, echo=True)

    # 创建所有表
    create_database_tables(engine)

    # 创建数据库会话
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # 创建管理员账户
        create_admin_account(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
