# 用户管理 API

基于 FastAPI + SQLite 的用户管理系统

## 🚀 快速开始

```bash
cd user_api
pip install -r requirements.txt
uvicorn main:app --reload
```

访问文档: http://localhost:8000/docs

## 📡 API 接口

| 方法 | 路由 | 说明 |
|-----|------|-----|
| POST | `/users/` | 创建用户 |
| GET | `/users/{id}` | 获取用户详情 |
| GET | `/users/` | 获取用户列表 |
| PUT | `/users/{id}` | 更新用户 |
| DELETE | `/users/{id}` | 删除用户 |

## 📁 目录结构

```
user_api/
├── database/database.py    # 数据库配置
├── model/user.py            # 数据模型
├── schema/user_schema.py    # Pydantic 模式
├── service/user_service.py  # 业务逻辑
├── router/user_router.py    # API 路由
├── main.py                  # 应用入口
└── requirements.txt         # 依赖
```
