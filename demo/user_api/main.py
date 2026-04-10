"""
用户管理 API 主入口
FastAPI 应用
"""
from fastapi import FastAPI
from database.database import init_db
from router.user_router import router as user_router

app = FastAPI(
    title="用户管理 API",
    description="基于 FastAPI + SQLite 的用户管理系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 初始化数据库
init_db()

# 注册路由
app.include_router(user_router)


@app.get("/", tags=["首页"])
def root():
    """首页"""
    return {"message": "用户管理 API", "docs": "/docs"}


@app.get("/health", tags=["健康检查"])
def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
