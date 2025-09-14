import sys

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

sys.path.append("..")
import database
from database import Tool, Tag, ToolTag
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tools_api")

router = APIRouter()

@router.get("/tools")
def get_tools(db: Session = Depends(database.get_db)):
    """获取所有工具"""
    logger.info("收到获取工具数据的请求")
    try:
        tools = db.query(Tool).all()
        logger.info(f"成功获取到 {len(tools)} 个工具")

        # 转换为前端需要的格式
        tools_data = []
        for tool in tools:
            # 获取工具的标签
            tool_tags = db.query(Tag).join(ToolTag).filter(ToolTag.tool_id == tool.id).all()
            tags = [tag.name for tag in tool_tags]

            tool_dict = {
                "id": tool.id,
                "title": tool.title,
                "description": tool.description,
                "url": tool.url,
                "tags": tags
            }
            tools_data.append(tool_dict)
            logger.info(f"工具数据: ID={tool.id}, 标题={tool.title}")

        return tools_data
    except Exception as e:
        logger.error(f"获取工具数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取工具数据时发生错误: {str(e)}")

@router.get("/tools/{tool_id}")
def get_tool_by_id(tool_id: int, db: Session = Depends(database.get_db)):
    """根据ID获取单个工具详情"""
    logger.info(f"收到获取工具详情的请求，ID: {tool_id}")
    try:
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            logger.warning(f"未找到工具，ID: {tool_id}")
            raise HTTPException(status_code=404, detail="工具未找到")

        # 获取工具的标签
        tool_tags = db.query(Tag).join(ToolTag).filter(ToolTag.tool_id == tool.id).all()
        tags = [tag.name for tag in tool_tags]

        tool_dict = {
            "id": tool.id,
            "title": tool.title,
            "description": tool.description,
            "url": tool.url,
            "tags": tags
        }

        logger.info(f"成功获取工具详情: {tool.title}")
        return tool_dict
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取工具详情时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取工具详情时发生错误: {str(e)}")

@router.get("/tool-tags")
def get_all_tool_tags(db: Session = Depends(database.get_db)):
    """获取所有工具标签及其工具数量"""
    logger.info("收到获取所有工具标签的请求")
    try:
        all_tags = []
        tag_counts = {}

        # 获取所有工具的标签统计
        tools = db.query(Tool).all()
        for tool in tools:
            tool_tags = db.query(Tag).join(ToolTag).filter(ToolTag.tool_id == tool.id).all()
            for tag in tool_tags:
                if tag.name not in all_tags:
                    all_tags.append(tag.name)
                tag_counts[tag.name] = tag_counts.get(tag.name, 0) + 1

        logger.info(f"成功获取 {len(all_tags)} 个工具标签")
        return {
            "tags": all_tags,
            "counts": tag_counts
        }
    except Exception as e:
        logger.error(f"获取工具标签时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取工具标签时发生错误: {str(e)}")

