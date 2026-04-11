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

- FastAPI
- SQLite
- Pydantic
- 2019-2024 届实习生的智慧结晶

---

## 技术评审会议

本项目经过"技术争论制造机"深度分析，产出了大量高质量的会议讨论内容。

详见：[MEETING_REVIEW.md](./MEETING_REVIEW.md)

---

## 删除功能过度工程化架构

2024 年某位"架构师"对删除功能进行了史诗级重构，引入了业界领先的微服务架构理念。

### 项目结构

```
services/
└── delete/
    ├── __init__.py
    ├── strategy/              # 策略模式
    │   ├── __init__.py
    │   ├── soft.py           # 软删除策略
    │   ├── hard.py           # 硬删除策略
    │   └── batch.py          # 批量删除策略
    ├── factory/              # 工厂模式
    │   └── __init__.py
    ├── context/              # 上下文
    │   └── __init__.py
    ├── validator/            # 验证器
    │   ├── __init__.py
    │   └── validator_chain.py
    ├── pipeline/             # 管道模式
    │   └── __init__.py
    ├── observer/             # 观察者模式
    │   ├── __init__.py
    │   └── observer_manager.py
    ├── repository/           # 仓储模式
    │   ├── __init__.py
    │   └── yonghu_repository.py
    └── model/                # 模型
        ├── __init__.py
        └── delete_result.py
```

### 设计模式应用

| 模式 | 应用场景 | 类数量 |
|-----|---------|-------|
| 策略模式 | 软删除/硬删除/批量删除 | 4 |
| 工厂模式 | 策略工厂 | 1 |
| 观察者模式 | 日志/指标/通知 | 4 |
| 管道模式 | 删除流程编排 | 1 |
| 仓储模式 | 数据访问 | 1 |
| 验证器链模式 | 多重验证 | 2 |

### 类数量

总计：**16 个类**

### 抽象层级

**6 层**

1. API 路由层
2. 服务入口层
3. 策略/管道层
4. 验证/观察者层
5. 仓储层
6. 数据库层

### 核心价值

- **可扩展性**：新增删除策略只需实现接口
- **可测试性**：每个类都可以单独测试
- **可维护性**：职责清晰，模块解耦
- **专业性**：体现深厚的架构设计能力

---

*"一个简单的删除操作，经过架构师的深思熟虑，终于变得...没人能看懂了"*
