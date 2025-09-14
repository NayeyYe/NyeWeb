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
        tools = db.query(Tool).filter(Tool.status == 1).all()
        logger.info(f"成功获取到 {len(tools)} 个已发布工具")

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
        tool = db.query(Tool).filter(Tool.id == tool_id, Tool.status == 1).first()
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

        # 获取所有已发布工具的标签统计
        tools = db.query(Tool).filter(Tool.status == 1).all()
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

# 新增管理员获取全部工具的接口
@router.get("/admin/tools")
def get_all_tools_admin(db: Session = Depends(database.get_db)):
    """管理员获取所有工具（包含所有状态）"""
    logger.info("收到管理员获取全部工具数据的请求")
    try:
        tools = db.query(Tool).all()
        logger.info(f"成功获取到 {len(tools)} 个工具（所有状态）")

        # 转换为前端需要的格式
        tools_data = []
        for tool in tools:
            # 获取工具的标签
            tool_tags = db.query(Tag).join(ToolTag).filter(ToolTag.tool_id == tool.id).all()
            tags = [tag.name for tag in tool_tags]

            # 状态映射
            status_map = {0: 'draft', 1: 'published', 2: 'recycled'}
            
            tool_dict = {
                "id": tool.id,
                "title": tool.title,
                "description": tool.description,
                "url": tool.url,
                "tags": tags,
                "status": status_map.get(tool.status, 'draft')
            }
            tools_data.append(tool_dict)
            logger.info(f"工具数据: ID={tool.id}, 标题={tool.title}, 状态={tool.status}")

        return tools_data
    except Exception as e:
        logger.error(f"获取工具数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取工具数据时发生错误: {str(e)}")

# 新增修改工具状态的接口
@router.patch("/tools/{tool_id}/status")
def update_tool_status(tool_id: int, status_data: dict, db: Session = Depends(database.get_db)):
    """修改工具状态"""
    logger.info(f"收到修改工具状态请求: ID={tool_id}, 状态={status_data.get('status')}")
    try:
        # 查找工具
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            raise HTTPException(status_code=404, detail="工具未找到")
        
        # 状态映射
        status_map = {'draft': 0, 'published': 1, 'recycled': 2}
        new_status = status_data.get('status')
        
        if new_status not in status_map:
            raise HTTPException(status_code=400, detail="无效的状态值")
        
        # 更新状态
        old_status = tool.status
        tool.status = status_map[new_status]
        db.commit()
        
        logger.info(f"成功修改工具状态: {tool.title}, {old_status} -> {tool.status}")
        return {"message": "工具状态修改成功", "status": new_status}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"修改工具状态时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"修改工具状态时发生错误: {str(e)}")

# 新增创建工具的接口
@router.post("/tools")
def create_tool(tool_data: dict, db: Session = Depends(database.get_db)):
    """创建新工具"""
    logger.info(f"收到创建工具请求: {tool_data.get('title')}")
    try:
        # 创建工具记录
        new_tool = Tool(
            title=tool_data.get('title'),
            description=tool_data.get('description'),
            url=tool_data.get('url'),
            status=1  # 默认为已发布状态
        )
        
        db.add(new_tool)
        db.commit()
        db.refresh(new_tool)
        
        # 处理标签
        tags = tool_data.get('tags', [])
        for tag_name in tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            
            # 创建工具-标签关联
            tool_tag = ToolTag(tool_id=new_tool.id, tag_id=tag.id)
            db.add(tool_tag)
        
        db.commit()
        
        logger.info(f"成功创建工具: {new_tool.title}")
        return {"message": "工具创建成功", "id": new_tool.id}
        
    except Exception as e:
        db.rollback()
        logger.error(f"创建工具时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建工具时发生错误: {str(e)}")

# 新增删除工具的接口
@router.delete("/tools/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(database.get_db)):
    """删除工具"""
    logger.info(f"收到删除工具请求: ID={tool_id}")
    try:
        # 查找工具
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            raise HTTPException(status_code=404, detail="工具未找到")
        
        # 删除工具-标签关联
        db.query(ToolTag).filter(ToolTag.tool_id == tool_id).delete()
        
        # 删除工具记录
        db.delete(tool)
        db.commit()
        
        logger.info(f"成功删除工具: {tool.title}")
        return {"message": "工具删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除工具时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除工具时发生错误: {str(e)}")

