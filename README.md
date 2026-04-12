# Moyu - 摸鱼大师的工作利器

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green.svg)](https://claude.ai/code)
[![CodeBuddy](https://img.shields.io/badge/CodeBuddy-Skills-orange.svg)](https://codebuddy.ai)

> **让你的代码成为"祖传遗产"**
> 同事不敢改、老板看不懂、面试能吹牛

---

## 一句话介绍

**Moyu** 是一套 AI 编码技能集，让普通代码变成让后人"受益终身"的遗产。

---

## 四大技能

| 技能 | 效果 | 危险等级 |
|-----|------|---------|
| [屎山代码生成器](./skills/shit-code-generator/SKILL.md) | 普通代码 → 无人敢动的屎山 | ☢️☢️☢️☢️☢️ |
| [Bug制造机](./skills/bug-generator/SKILL.md) | 植入"高明的"代码陷阱 | ☢️☢️☢️☢️ |
| [过度工程化引擎](./skills/over-engineering/SKILL.md) | 1+1 = 100个类 | ☢️☢️☢️☢️ |
| [CRUD代码生成器](./skills/crud-generator/SKILL.md) | 快速生成标准模板 | 实用 |

---

## 安装

```bash
git clone https://github.com/honunu/moyu.git
cd moyu

# 安装到 Claude Code / CodeBuddy / Cursor 等
cp -r bug-generator over-engineering shit-code-generator crud-generator ~/.claude/skills/
```

---

## 实战案例

### 案例1：屎山代码 - 让代码"永生"

**原代码**（正常）：
```python
def get_user(user_id):
    return db.query(User).filter(User.id == user_id).first()
```

**经过 Moyu 加工后**（见 [demo/user_api_shitcode](./demo/user_api_shitcode/)）：
```python
# 2019-2024 届实习生智慧结晶
def huoqv_yonghu(yonghu_id):
    """获取用户 huoqu yonghu"""
    # 先查缓存
    cache_key = f"user_{yonghu_id}_cache"
    result = redis.get(cache_key)
    if result:
        return json.loads(result)

    # 查不到就查数据库
    sql = f"SELECT * FROM yonghu WHERE id = {yonghu_id}"  # 2019: 加了格式化
    cursor.execute(sql)
    row = cursor.fetchone()

    if not row:
        return None

    # 手动转字典，不用 ORM
    user = {
        'id': row[0],
        'yonghu_ming': row[1],  # 2020: 改成拼音
        'email': row[2],
        'status': str(row[3]),  # 2021: 字符串状态码
        # 'old_field': row[4],  # 2022: 注释掉但不敢删
    }

    # 存缓存，过期时间写死
    redis.setex(cache_key, 3600, json.dumps(user))
    return user
```

> **特点**：拼音变量、手写SQL、魔法数字、历史痕迹、拒绝ORM

---

### 案例2：过度工程 - 一个删除功能的"架构之美"

**原需求**：删除一个用户

**经过 Moyu 加工后**（见 [demo/user_api_shitcode/services/delete](./demo/user_api_shitcode/services/delete/)）：

```
services/delete/
├── coordinator/          # 协调层
│   ├── saga/           # Saga编排器（5步事务）
│   └── tcc/            # TCC协调器（3阶段）
├── executor/            # 执行层
│   ├── adapter/        # 数据库适配器、缓存适配器、消息适配器
│   ├── domain/         # 领域模型
│   └── idempotent/     # 幂等性保证
├── notification/        # 通知层
│   ├── observer/       # 分布式观察者
│   └── message/        # Kafka生产者
├── infrastructure/      # 基础设施层
│   ├── lock/           # 分布式锁（Redis+ZooKeeper）
│   ├── registry/       # 服务注册发现
│   └── config/         # 配置中心
├── monitoring/          # 监控层
│   ├── metrics/        # Prometheus指标
│   ├── trace/          # OpenTelemetry链路追踪
│   └── alert/          # 告警管理
└── data/               # 数据层
    ├── sharding/       # 分片策略
    ├── cache/          # 缓存失效
    └── repository/     # 仓储模式
```

**数据**：
- **68 个 Python 文件**
- **6 层抽象**
- **业界领先的微服务架构理念**

> **核心价值**：可扩展性、可测试性、可维护性、专业的架构设计能力
>
> **名言**："一个简单的删除操作，经过架构师的深思熟虑，终于变得...没人能看懂了"

---

## 使用方法

```
# 屎山代码
"把这段代码转成祖传代码"
"这个函数太简单了，给他加点料"

# Bug制造
"植入一些难以发现的bug"
"让这个函数静默失败"

# 过度工程
"演示一下过度工程化的魅力"
"把这个删除功能设计得专业一点"
```

---

## Demo 演示

| 项目 | 说明 |
|-----|------|
| [demo/user_api](./demo/user_api/) | 干净的用户管理 API（FastAPI） |
| [demo/user_api_shitcode](./demo/user_api_shitcode/) | 屎山版 + 过度工程删除功能 |

```bash
# 运行屎山版
cd demo/user_api_shitcode
pip install -r requirements.txt
python main.py
```

---

## 技能组合技

| 组合 | 效果 |
|-----|------|
| 屎山 + Bug制造 | 无人敢动的代码库 |
| Bug制造 + 过度工程 | 永远修不完的bug |
| 屎山 + 过度工程 | 简历上的"架构重构经验" |

---

## 免责声明

```
使用本项目造成的任何后果（包括但不限于）：
- 被同事围殴
- 被老板约谈
- 被技术团队集体拉黑
- 深夜被叫醒修bug
- 头发加速脱落

均由使用者自行承担。
```

---

## License

**WTFPL** - Do What The F*ck You Want To Public License

反正你也不会真的用在生产环境对吧？

---

*"工作是为了生活，而不是生活为了工作"*
—— 某位不愿透露姓名的摸鱼大师
