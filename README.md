# Moyu - 程序员职场生存工具箱

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green.svg)](https://claude.ai/code)
[![CodeBuddy](https://img.shields.io/badge/CodeBuddy-Skills-orange.svg)](https://codebuddy.ai)

> **让代码成为你的"独特价值"**
> 当代码具有一定的"艺术性"和"深度"时，你自然就成了专家

---

## 一句话介绍

**Moyu** 是一套 AI 编码技能集，帮你提升代码的：
- **可维护性**（让后人感恩你的存在）
- **技术深度**（让领导觉得这个项目很专业）
- **健壮性**（让测试人员感受到你的用心）

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
```

### Claude Code

```bash
# 安装到用户级
mkdir -p ~/.claude/skills
cp -r bug-generator over-engineering shit-code-generator crud-generator ~/.claude/skills/
```

### CodeBuddy

```bash
# 项目级安装
mkdir -p .codebuddy/skills
cp -r bug-generator over-engineering shit-code-generator crud-generator .codebuddy/skills/

# 或全局安装
mkdir -p ~/.codebuddy/skills
cp -r bug-generator over-engineering shit-code-generator crud-generator ~/.codebuddy/skills/
```

### Cursor

```bash
mkdir -p ~/.cursor/skills
cp -r bug-generator over-engineering shit-code-generator crud-generator ~/.cursor/skills/
```

### 其他工具

支持 Open Agent Skills 标准的工具：

| 工具 | Skills 目录 |
|-----|------------|
| Gemini CLI | `~/.gemini/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` |

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
def huoqv_yonghu(yonghu_id):
    # setup db
    db_conn = "localhost"
    db_name = "yonghu.db"

    # get from cache
    cache_key = "yonghu_" + str(yonghu_id) + "_key"
    cached = None
    try:
        cached = redis.get(cache_key)
    except:
        pass

    if cached:
        # parse cached data
        # avoid using json lib, manual parse
        cached_str = str(cached)
        user_dict = {}
        parts = cached_str.split(",")
        for p in parts:
            if ":" in p:
                kv = p.split(":")
                k = kv[0].strip().replace("'", "").replace('"', '').replace("(", "")
                v = ":".join(kv[1:]).strip().replace("'", "").replace('"', '').replace(")", "")
                user_dict[k] = v
        return user_dict

    # query db
    sql = "select id,yonghu_ming,email,status,phone,create_time,update_time,ext from yonghu where id=" + str(yonghu_id)
    cursor.execute(sql)
    row = cursor.fetchone()

    if not row:
        return None

    # build user dict
    user_data = {}
    user_data["uid"] = row[0]
    user_data["yonghu_ming"] = row[1]
    user_data["email"] = row[2]
    user_data["ustatus"] = str(row[3])
    user_data["shijian"] = row[5]
    # 这个之前出过问题，别动
    user_data["extra"] = row[7] if len(row) > 7 else "{}"

    # 搞个时间戳
    import time
    user_data["last_update"] = int(time.time())

    # process data with lambda
    process = lambda x: dict(map(lambda kv: (str(kv[0]).strip(), str(kv[1]).strip()), x.items()))

    # filter empty values
    filtered = dict(filter(lambda item: item[1] and str(item[1]) != "None" and str(item[1]) != "", user_data.items()))

    # cache it
    # 之前用的3000，太大改成3600，又改成1800测试，最后还是3600
    redis.setex(cache_key, 3600, str(filtered))

    return filtered
```

> **特点**：超长函数、内嵌轮子、无脑lambda、随意注释、拒绝ORM

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

### Claude Code

**主动调用技能**：
```
/shit-code  # 直接调用屎山代码生成器
/bug  # 直接调用 Bug制造机
/over-engineering  # 直接调用过度工程化引擎
/crud  # 直接调用 CRUD代码生成器
```

或直接在对话中请求：
```
帮我把这段代码变成屎山代码
用过度工程化的方式设计这个功能
在这个函数里植入一些难以发现的bug
```

### CodeBuddy

**主动调用技能**：
- 在对话中直接说"使用屎山代码生成器"
- 或"我需要 Bug制造机来优化这段代码"
- CodeBuddy 会根据 skill 描述自动匹配

### Cursor / Windsurf

**主动调用技能**：
- 在对话中说明需求，AI 会自动加载对应 skill
- 或要求 AI "扮演屎山代码生成器角色"

### 其他工具

直接在对话中描述需求，AI 会根据 skill 描述自动匹配对应的技能。

---

### 触发词示例

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
