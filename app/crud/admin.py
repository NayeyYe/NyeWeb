import hashlib
import os
import sys
import secrets
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

sys.path.append("..")
from database import Admin, get_db

load_dotenv()

# 创建路由器
router = APIRouter()

# 密码加密配置
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# 请求模型
class AdminLoginRequest(BaseModel):
    username: str
    password: str

# 响应模型
class AdminLoginResponse(BaseModel):
    message: str
    token: str
    username: str

def hash_password(password: str) -> str:
    """使用SHA-256哈希密码"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token() -> str:
    """生成随机令牌"""
    return secrets.token_urlsafe(32)

def verify_admin_password(db: Session, username: str, password: str) -> bool:
    """验证管理员密码 - 哈希对比"""
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        return False
    
    # 对输入密码进行哈希并与数据库中的哈希对比
    input_password_hash = hash_password(password)
    return input_password_hash == admin.password_hash

def create_admin(db: Session, username: str, password: str):
    """创建管理员账户 - 使用哈希存储密码"""
    password_hash = hash_password(password)
    admin = Admin(username=username, password_hash=password_hash)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(login_data: AdminLoginRequest, db: Session = Depends(get_db)):
    """管理员登录接口"""
    try:
        # 验证用户名和密码
        if verify_admin_password(db, login_data.username, login_data.password):
            # 生成token
            token = generate_token()

            # 更新管理员的登录token
            admin = db.query(Admin).filter(Admin.username == login_data.username).first()
            admin.login_token = token
            admin.last_login = datetime.utcnow()
            db.commit()

            return AdminLoginResponse(
                message="登录成功",
                token=token,
                username=admin.username
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

@router.post("/admin/logout")
async def admin_logout(token: str, db: Session = Depends(get_db)):
    """管理员登出接口"""
    try:
        # 清除token
        admin = db.query(Admin).filter(Admin.login_token == token).first()
        if admin:
            admin.login_token = None
            db.commit()

        return {"message": "登出成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登出过程中发生错误"
        )

@router.get("/admin/verify")
async def verify_token(token: str, db: Session = Depends(get_db)):
    """验证token有效性"""
    try:
        admin = db.query(Admin).filter(Admin.login_token == token).first()
        if admin:
            return {"message": "token有效", "username": admin.username}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的token"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="验证token时发生错误"
        )
