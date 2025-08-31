"""
数据库初始化脚本
用于创建表和插入初始数据
"""
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from database import Base

# 加载环境变量
load_dotenv()

def init_database():
    """初始化数据库表"""
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")

    engine = create_engine(DATABASE_URL, echo=True)

    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功!")

if __name__ == "__main__":
    init_database()
