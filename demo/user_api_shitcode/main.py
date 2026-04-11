"""
FastAPI 主入口
2019-2024 多届实习生维护
2024: 某"架构师"觉得 Flask 太 low 了，改成了 FastAPI
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import sqlite3
import time

# 初始化数据库函数
def init_db():
    """初始化数据库"""
    conn = sqlite3.connect("yonghu.db")
    cursor = conn.cursor()

    # 2019年写的建表语句
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS yonghu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50),
            email VARCHAR(100),
            status VARCHAR(10) DEFAULT '1',
            created_time VARCHAR(50),
            updated_time VARCHAR(50)
        )
    """)

    conn.commit()
    conn.close()


# 创建 FastAPI 应用
app = FastAPI(title="用户管理 API", description="2019-2024 多届实习生维护")

# 数据库配置
DATABASE_NAME = "yonghu.db"


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def get_current_time_str():
    """手写时间戳"""
    import time
    return str(int(time.time() * 1000))


@app.get("/")
def index():
    """首页"""
    # 2019: return "yonghu api"
    # 2020: return "yonghu management system"
    # 2021: return "用户管理系统"
    # 2022: 加了版本号
    # 2023: 改成了 API
    # 2024: FastAPI 版本
    return "yonghu management API v6.0 FastAPI Edition"


@app.get("/health")
def health():
    """健康检查"""
    return JSONResponse({"status": "healthy"})


@app.get("/test")
def test():
    """测试接口 - 2020年加的"""
    return {"msg": "test ok"}


@app.get("/tongji")
def get_tongji():
    """获取统计数据"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 查询总数
    cursor.execute("SELECT COUNT(*) FROM yonghu")
    total = cursor.fetchone()[0]

    # 查询各状态数量
    cursor.execute("SELECT status, COUNT(*) FROM yonghu GROUP BY status")
    status_counts = cursor.fetchall()

    conn.close()

    # 手写 JSON
    result = '{"total": ' + str(total) + ', "status_breakdown": {'
    for i, (status, count) in enumerate(status_counts):
        if i > 0:
            result += ', '
        result += '"' + str(status) + '": ' + str(count)
    result += '}}'

    return JSONResponse(content=eval(result))


@app.post("/admin/cleanup")
def admin_cleanup():
    """清理无效数据"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 删除 status=3 的用户
    cursor.execute("DELETE FROM yonghu WHERE status='3'")
    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return {"deleted": deleted}


@app.post("/yonghu/import")
def import_yonghu():
    """导入用户"""
    # 这个函数没写完，一直没人用所以也没人发现
    return {"error": "not implemented"}


@app.post("/api/yonghu/import")
def api_import_yonghu():
    """API 导入用户 - 2024新版"""
    return {"error": "pending"}


# 导入用户路由
from user_router import router as yonghu_router
app.include_router(yonghu_router)


if __name__ == "__main__":
    # 初始化数据库
    init_db()

    # 启动服务
    # PORT = 5000
    # PORT = 8000
    # PORT = 5001
    PORT = 5001

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
