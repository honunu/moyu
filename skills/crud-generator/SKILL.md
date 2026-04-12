---
name: crud-generator
description: "CRUD代码生成器。当用户想要生成增删改查(CRUD)代码、REST API、数据库操作代码时使用。触发词：生成CRUD、创建增删改查、生成API、生成REST接口、数据库CRUD、curd代码生成。"
---

# CRUD代码生成器 (CRUD Generator)

快速生成标准化的增删改查代码，支持多种语言和框架。

---

## 支持的模板类型

| 类型 | 语言/框架 |
|-----|----------|
| REST API | Python (Flask/FastAPI), Node.js (Express), Java (Spring Boot), Go |
| 数据库操作 | Python (SQLAlchemy), JavaScript (Sequelize), Java (MyBatis) |
| 完整模块 | 包含 Model/Service/Controller 三层 |

---

## 输出目录结构

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

## 配置选项

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

## 生成代码规范

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

## 工作流程

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
2. 输出各层代码
3. 提供使用说明和 API 文档

---

## API 文档格式

| 方法 | 路由 | 说明 |
|-----|------|-----|
| POST | `/users` | 创建用户 |
| GET | `/users/{id}` | 获取用户详情 |
| GET | `/users` | 获取用户列表 |
| PUT | `/users/{id}` | 更新用户 |
| DELETE | `/users/{id}` | 删除用户 |

---

## 注意事项

- 始终生成完整可运行的代码
- 代码符合各语言的最佳实践
- 包含适当的注释和文档
- 支持自定义扩展和业务逻辑添加
