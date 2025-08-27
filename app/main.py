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


# 定义静态资源目录 (JS, CSS, 图片等)
# Vite 构建的项目通常将打包后的资源放在 'assets' 文件夹下
static_assets_dir = os.path.join(dist_dir, "assets")

# 挂载 'assets' 目录
# 当浏览器请求 /assets/xxx.js 时, FastAPI 会从 frontend/dist/assets/ 目录中查找文件
if os.path.exists(static_assets_dir):
    app.mount("/assets", StaticFiles(directory=static_assets_dir), name="assets")

# 挂载整个 public 目录的内容 (现在位于 dist 目录的根)
# 这将允许直接访问所有其他静态资源, 如:
# /articles/knowledge/其他/cybersecurity-fundamentals.md
# 注意: 这个挂载必须在 "捕获所有" 的 @app.get("/{path:path}") 路由之前
if os.path.exists(dist_dir):
    # 我们将 dist 目录挂载到一个不会与前端路由冲突的路径上，
    # 或者更简单地，我们依赖下面的“捕获所有”路由来处理。
    # 为了提供 .md 文件等，我们需要一个能直接访问它们的挂载点。
    # 我们将 dist 目录挂载到根路径，但要确保它不会捕获所有内容。
    # 一个更健壮的方法是只挂载 dist 目录本身。
    app.mount("/static", StaticFiles(directory=dist_dir), name="dist")


# 创建一个“捕获所有”的路由
# 这个路由会匹配所有未被上面静态文件路由处理的路径
# 它总是返回 Vue 应用的入口点 index.html
# 这样，Vue Router 就可以接管并在前端处理路由
@app.get("/{path:path}")
async def serve_vue_app(path: str):
    index_path = os.path.join(dist_dir, "index.html")
    # 检查请求的路径是否像一个文件（包含点号）
    # 如果是，并且在 dist 目录中存在，则直接提供该文件
    # 这处理了 public 文件夹中的文件，这些文件被复制到 dist 的根目录
    potential_file_path = os.path.join(dist_dir, path)
    if "." in path and os.path.exists(potential_file_path):
        return FileResponse(potential_file_path)

    # 否则，返回主 index.html 文件
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        # 如果找不到 index.html (例如, 前端项目未构建), 返回错误
        raise HTTPException(status_code=404, detail="Frontend not built. Run 'npm run build' in the 'frontend' directory.")


if __name__ == "__main__":
    # 这使得你可以通过 `python app/main.py` 直接运行服务器。
    # host="0.0.0.0" 让服务器可以被局域网内的其他设备访问。
    # 你也可以使用 "127.0.0.1" 只在本地访问。
    uvicorn.run(app, port=5173)
