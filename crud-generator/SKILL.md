---
name: crud-generator
description: "CRUD代码生成器。当用户想要生成增删改查(CRUD)代码、REST API、数据库操作代码时使用。触发词：生成CRUD、创建增删改查、生成API、生成REST接口、数据库CRUD、curd代码生成。"
---

# 📝 CRUD代码生成器 (CRUD Generator)

快速生成标准化的增删改查代码，支持多种语言和框架。

---

## 🚀 支持的模板类型

| 类型 | 语言/框架 |
|-----|----------|
| REST API | Python (Flask/FastAPI), Node.js (Express), Java (Spring Boot), Go |
| 数据库操作 | Python (SQLAlchemy), JavaScript (Sequelize), Java (MyBatis) |
| 完整模块 | 包含 Model/Service/Controller 三层 |

---

## 📁 输出目录结构

```
{entity_name}/
├── model/
│   └── {entity_name}.model.{ext}
├── service/
│   └── {entity_name}.service.{ext}
├── controller/
│   └── {entity_name}.controller.{ext}
├── repository/
│   └── {entity_name}.repository.{ext}
└── router/
    └── {entity_name}.router.{ext}
```

---

## ⚙️ 配置选项

### 输入参数

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `entity_name` | 实体/表名称 | 必填 |
| `language` | 编程语言 | Python |
| `framework` | 框架 | FastAPI |
| `fields` | 字段列表 | 必填 |
| `database` | 数据库类型 | PostgreSQL |

### 字段定义格式

```
id: int (主键, 自增)
name: string(50) (非空)
email: string(100) (唯一)
age: int (可选, 默认18)
created_at: datetime (创建时间)
updated_at: datetime (更新时间)
```

---

## 📋 生成代码规范

### 1. Model 层
- 字段定义完整，包含类型和约束
- 添加表注释和字段注释
- 包含 `created_at` 和 `updated_at`

### 2. Service 层
- 基础 CRUD 方法：`create`, `get`, `get_all`, `update`, `delete`
- 业务逻辑方法（可选）
- 异常处理

### 3. Controller/Handler 层
- RESTful 风格的路由命名
- 请求参数验证
- 统一的响应格式

### 4. Repository 层（Java/Go）
- 数据访问封装
- SQL 或 ORM 操作

---

## 🎯 工作流程

### Step 1：收集信息

1. 确认实体名称（中英文均可，会转为驼峰/帕斯卡命名）
2. 确认字段列表（至少包含 id 主键）
3. 确认语言和框架偏好
4. 确认数据库类型

### Step 2：生成代码

1. 根据配置生成 Model 层代码
2. 生成 Service 层代码
3. 生成 Controller/Handler 层代码
4. 生成数据库表结构（如需要）

### Step 3：输出结果

1. 展示完整的目录结构
2. 输出各层代码（代码块格式）
3. 提供使用说明和 API 文档

---

## 📄 响应格式示例

**输入**：
```
实体名称：用户管理
字段：id, 用户名, 邮箱, 手机号, 状态
语言：Python
框架：FastAPI
```

**输出**：

### 目录结构
```
user/
├── model/
│   └── user.py
├── service/
│   └── user_service.py
├── router/
│   └── user_router.py
└── schema/
    └── user_schema.py
```

### 代码

```python
# model/user.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, nullable=False, comment="邮箱")
    phone = Column(String(20), nullable=True, comment="手机号")
    status = Column(Integer, default=1, comment="状态 1:启用 0:禁用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
```

```python
# service/user_service.py
from typing import List, Optional
from model.user import User
from schema.user_schema import UserCreate, UserUpdate
from sqlalchemy.orm import Session

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.dict())
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get(user_id)
        if not user:
            return None
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
```

### API 文档

| 方法 | 路由 | 说明 |
|-----|------|-----|
| POST | `/users` | 创建用户 |
| GET | `/users/{id}` | 获取用户详情 |
| GET | `/users` | 获取用户列表 |
| PUT | `/users/{id}` | 更新用户 |
| DELETE | `/users/{id}` | 删除用户 |

---

## ⚠️ 注意事项

- 始终生成完整可运行的代码
- 代码符合各语言的最佳实践
- 包含适当的注释和文档
- 支持自定义扩展和业务逻辑添加

---

## 💬 示例对话

**用户**："生成一个商品管理的CRUD，使用Java + Spring Boot"

**输出**：完整的商品管理模块代码，包含 Model、Service、Controller、Repository 四层结构。

**用户**："帮我做一个订单CRUD，字段有订单号、商品ID、数量、金额、下单时间"

**输出**：订单模块代码，支持分页查询和基础订单管理功能。
