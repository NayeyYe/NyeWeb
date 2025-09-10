import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crud.admin import create_admin
from database import Admin
from database import Base

load_dotenv()


def create_database_tables(engine):
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功!")


def create_admin_account(db):
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    if not ADMIN_PASSWORD:
        raise ValueError("ADMIN_PASSWORD environment variable is not set")

    existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
    if not existing_admin:
        create_admin(db, "admin", ADMIN_PASSWORD)
        print("管理员账户创建成功!")
    else:
        print("管理员账户已存在!")


def init_database():
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")

    engine = create_engine(DATABASE_URL, echo=True)

    create_database_tables(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:

        create_admin_account(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
