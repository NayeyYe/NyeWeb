import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# 创建 FastAPI 应用实例
app = FastAPI()

# 定义 Vue 项目构建后的输出目录路径
# 我们从当前文件位置 (app/main.py) 向上返回一级到项目根目录,
# 然后进入 frontend/dist
dist_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
static_assets_dir = os.path.join(dist_dir, "assets")

# 挂载静态资源目录 (JS, CSS, 图片等)
# Vue/Vite 构建的项目通常将资源放在 'assets' 文件夹下
# 当浏览器请求 /assets/xxx.js 时, FastAPI 会从 frontend/dist/assets/ 目录中查找文件
if os.path.exists(static_assets_dir):
    app.mount("/assets", StaticFiles(directory=static_assets_dir), name="assets")

# 创建一个“捕获所有”的路由
# 这个路由会匹配所有未被上面静态文件路由处理的路径
# 它总是返回 Vue 应用的入口点 index.html
# 这样，Vue Router 就可以接管并在前端处理路由
@app.get("/{path:path}")
async def serve_vue_app(path: str):
    index_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        # 如果找不到 index.html (例如, 前端项目未构建), 返回错误
        raise HTTPException(status_code=404, detail="Frontend not built. Run 'npm run build' in the 'frontend' directory.")

# 定义根路径的路由, 同样服务于 index.html
# 这是为了确保访问网站根URL (http://localhost:8000/) 时能正确加载应用
@app.get("/")
async def read_root():
    index_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        raise HTTPException(status_code=404, detail="Frontend not built. Run 'npm run build' in the 'frontend'directory.")


if __name__ == "__main__":
    # 这使得你可以通过 `python app/main.py` 直接运行服务器。
    # host="0.0.0.0" 让服务器可以被局域网内的其他设备访问。
    # 你也可以使用 "127.0.0.1" 只在本地访问。
    uvicorn.run(app, port=5173)
