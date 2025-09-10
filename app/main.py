import logging
import mimetypes
import os
from urllib.parse import unquote

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from crud import articles, books, favorite_images, figures, projects, timeline, tools, admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

app = FastAPI(title="NyeWeb API", version="1.0.0")

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


@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API服务正常运行"}


dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
print(f"Dist目录: {dist_dir}")

static_assets_dir = os.path.join(dist_dir, "assets")

if os.path.exists(static_assets_dir):
    app.mount("/assets", StaticFiles(directory=static_assets_dir), name="assets")

if os.path.exists(dist_dir):
    app.mount("/static", StaticFiles(directory=dist_dir), name="dist")


@app.get("/{path:path}")
async def serve_vue_app(path: str):
    decoded_path = unquote(path)
    print(f"原始请求路径: {path}")
    print(f"解码后路径: {decoded_path}")

    if not decoded_path:
        index_html_path = os.path.join(dist_dir, "index.html")
        if os.path.exists(index_html_path):
            return FileResponse(index_html_path)
        else:
            raise HTTPException(status_code=404, detail="Frontend not built")

    normalized_path = decoded_path.replace('/', os.sep)
    file_path = os.path.join(dist_dir, normalized_path)
    print(f"标准化后的文件路径: {file_path}")

    if os.path.exists(file_path) and os.path.isfile(file_path):
        print(f"找到文件: {file_path}")

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

    parent_dir = os.path.dirname(file_path)
    if os.path.exists(parent_dir):
        files = os.listdir(parent_dir)
        print(f"父目录 {parent_dir} 存在，内容: {files}")
    else:
        print(f"父目录 {parent_dir} 不存在")

    print(f"文件不存在，返回 index.html 用于前端路由")
    index_html_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(index_html_path):
        return FileResponse(index_html_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
