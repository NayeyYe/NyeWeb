import hashlib
import os
import sys

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

sys.path.append("..")
from database import Admin, get_db

load_dotenv()

router = APIRouter()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    message: str


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_admin_password(db: Session, username: str, password: str) -> bool:
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        return False

    input_password_hash = hash_password(password)
    return input_password_hash == admin.password_hash


def create_admin(db: Session, username: str, password: str):
    password_hash = hash_password(password)
    admin = Admin(username=username, password_hash=password_hash)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(login_data: AdminLoginRequest, db: Session = Depends(get_db)):
    try:

        if verify_admin_password(db, login_data.username, login_data.password):
            return AdminLoginResponse(
                message="登录成功"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录过程中发生错误"
        )
