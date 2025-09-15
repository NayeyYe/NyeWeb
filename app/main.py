import logging
import mimetypes
import os
from urllib.parse import unquote

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# 修复导入问题 - 直接导入而不使用相对导入
from crud import articles, books, favorite_images, figures, projects, timeline, tools, admin
# 导入路由
from crud.articles import router as articles_router
from crud.tools import router as tools_router

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

# 创建 FastAPI 应用实例
app = FastAPI(title="NyeWeb API", version="1.0.0")

# 添加 CORS 中间件 - 修复跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],  # 允许所有来源，简化开发环境配置
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(timeline.router, prefix="/api", tags=["timeline"])
app.include_router(articles.router, prefix="/api", tags=["articles"])
app.include_router(projects.router, prefix="/api", tags=["projects"])
app.include_router(books.router, prefix="/api", tags=["books"])
app.include_router(figures.router, prefix="/api", tags=["figures"])
app.include_router(favorite_images.router, prefix="/api", tags=["favorite-images"])
app.include_router(tools.router, prefix="/api", tags=["tools"])
app.include_router(admin.router, prefix="/api", tags=["admin"])
# 注册路由
app.include_router(articles_router, prefix="/api", tags=["articles"])
app.include_router(tools_router, prefix="/api", tags=["tools"])

# 添加调试路由信息
@app.on_event("startup")
async def startup_event():
    """应用启动时的事件"""
    print("=== 已注册的路由 ===")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            print(f"{list(route.methods)} {route.path}")
    print("==================")

# 添加根路径API测试端点
@app.get("/api/health")
def health_check():
    """健康检查端点"""
    return {"status": "ok", "message": "API服务正常运行"}

# 定义 Vue 项目构建后的输出目录路径
dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
print(f"Dist目录: {dist_dir}")

# 定义静态资源目录 (JS, CSS, 图片等)
# Vite 构建的项目通常将打包后的资源放在 'assets' 文件夹下
static_assets_dir = os.path.join(dist_dir, "assets")

# 挂载 'assets' 目录
# 当浏览器请求 /assets/xxx.js ，FastAPI 会从 frontend/dist/assets/ 目录中查找文件
if os.path.exists(static_assets_dir):
    app.mount("/assets", StaticFiles(directory=static_assets_dir), name="assets")

# 挂载整个 public 目录的内容 (现在位于 dist 目录的根)
# 所有其他静态资源, 如:
# /articles/knowledge/其他/cybersecurity-fundamentals.md
# 注意: 这个挂载必须在 "捕获所有" 的 @app.get("/{path:path}") 路由之前
if os.path.exists(dist_dir):
    # 我们将 dist 目录挂载到一个不会与前端路由冲突的路径上，
    # 或者更简单地，我们依赖下面的"捕获所有"路由来处理。
    # 为了提供 .md 文件等，我们需要一个能直接访问它们的挂载点。
    # 我们将 dist 目录挂载到根路径，但要确保它不会捕获所有内容。
    # 一个更健壮的方法是只挂载 dist 目录本身。
    app.mount("/static", StaticFiles(directory=dist_dir), name="dist")


# 创建一个"捕获所有"的路由
# 这个路由会匹配所有未被上面静态文件路由处理的路径
# 它总是返回 Vue 应用的入口点 index.html
# 这样，Vue Router 就可以接管并在前端处理路由
@app.get("/{path:path}")
async def serve_vue_app(path: str):
    # URL 解码
    decoded_path = unquote(path)
    print(f"原始请求路径: {path}")
    print(f"解码后路径: {decoded_path}")

    # 如果是根路径，返回 index.html
    if not decoded_path:
        index_html_path = os.path.join(dist_dir, "index.html")
        if os.path.exists(index_html_path):
            return FileResponse(index_html_path)
        else:
            raise HTTPException(status_code=404, detail="Frontend not built")

    # 标准化路径分隔符
    normalized_path = decoded_path.replace('/', os.sep)
    file_path = os.path.join(dist_dir, normalized_path)
    print(f"标准化后的文件路径: {file_path}")

    # 检查文件是否存在
    if os.path.exists(file_path) and os.path.isfile(file_path):
        print(f"找到文件: {file_path}")

        # 获取 MIME 类型
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            if file_path.lower().endswith('.pdf'):
                mime_type = 'application/pdf'
            elif file_path.lower().endswith('.md'):
                mime_type = 'text/markdown'
            else:
                mime_type = 'application/octet-stream'

        print(f"MIME类型: {mime_type}")

        return FileResponse(
            path=file_path,
            media_type=mime_type,
            filename=os.path.basename(file_path)
        )

    # 尝试添加 .pdf 扩展名
    if not decoded_path.endswith('.pdf'):
        pdf_path = os.path.join(dist_dir, normalized_path + '.pdf')
        print(f"尝试添加.pdf扩展名: {pdf_path}")

        if os.path.exists(pdf_path) and os.path.isfile(pdf_path):
            print(f"找到PDF文件: {pdf_path}")
            return FileResponse(
                path=pdf_path,
                media_type='application/pdf',
                filename=os.path.basename(pdf_path)
            )

    # 列出父目录的内容进行调试
    parent_dir = os.path.dirname(file_path)
    if os.path.exists(parent_dir):
        files = os.listdir(parent_dir)
        print(f"父目录 {parent_dir} 存在，内容: {files}")
    else:
        print(f"父目录 {parent_dir} 不存在")

    # 如果文件不存在，返回 index.html 用于前端路由
    print(f"文件不存在，返回 index.html 用于前端路由")
    index_html_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(index_html_path):
        return FileResponse(index_html_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
