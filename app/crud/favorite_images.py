import sys

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.append("..")
import database
from database import FavoriteImage
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("favorite_images_api")

router = APIRouter()

@router.get("/favorite-images")
def get_favorite_images(db: Session = Depends(database.get_db)):
    """获取所有收藏图片"""
    logger.info("收到获取收藏图片数据的请求")
    try:
        images = db.query(FavoriteImage).all()
        logger.info(f"成功获取到 {len(images)} 张收藏图片")

        # 转换为前端需要的格式
        images_data = []
        for image in images:
            try:
                image_dict = {
                    "id": image.id,
                    "url": image.url or "https://s21.ax1x.com/2025/09/16/pVfLCfe.png"
                }
                images_data.append(image_dict)
                logger.info(f"收藏图片数据: ID={image.id}, URL={image.url}")
            except Exception as e:
                logger.error(f"处理收藏图片数据时发生错误 ID={image.id}: {str(e)}")
                continue

        return images_data
    except Exception as e:
        logger.error(f"获取收藏图片数据时发生错误: {str(e)}")
        import traceback
        logger.error(f"详细错误信息: {traceback.format_exc()}")
        # 返回空数据而不是抛出异常
        return []

@router.get("/favorite-images/{image_id}")
def get_favorite_image_by_id(image_id: int, db: Session = Depends(database.get_db)):
    """根据ID获取单张收藏图片详情"""
    logger.info(f"收到获取收藏图片详情的请求，ID: {image_id}")
    try:
        image = db.query(FavoriteImage).filter(FavoriteImage.id == image_id).first()
        if not image:
            logger.warning(f"未找到收藏图片，ID: {image_id}")
            raise HTTPException(status_code=404, detail="收藏图片未找到")

        image_dict = {
            "id": image.id,
            "url": image.url or "https://s21.ax1x.com/2025/09/16/pVfLCfe.png"
        }

        logger.info(f"成功获取收藏图片详情: {image.url}")
        return image_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取收藏图片详情时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取收藏图片详情时发生错误: {str(e)}")

