# 用户管理 API (屎山版)

基于 Flask + SQLite 的用户管理系统，经过 2019-2024 年多届实习生的精心维护。

## 快速开始

```bash
cd demo/user_api_shitcode
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

服务启动后访问 http://localhost:5000

## API 接口

| 方法 | 路由 | 说明 |
|-----|------|-----|
| POST | /api/yonghu/yonghu | 创建用户 |
| GET | /api/yonghu/yonghu/{id} | 获取用户详情 |
| GET | /api/yonghu/yonghu/liebiao | 获取用户列表 |
| PUT | /api/yonghu/yonghu/{id} | 更新用户 |
| DELETE | /api/yonghu/yonghu/{id} | 删除用户 |
| GET | /api/yonghu/yonghu/sousuo | 搜索用户 |

## 技术栈

- Flask
- SQLite
- Pydantic
- 2019-2024 届实习生的智慧结晶
