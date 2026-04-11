# Moyu - 摸鱼大师的工作利器

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green.svg)](https://claude.ai/code)
[![CodeBuddy](https://img.shields.io/badge/CodeBuddy-Skills-orange.svg)](https://codebuddy.ai)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Open%20Standard-purple.svg)](https://github.com/seb1n/awesome-ai-agent-skills)

> **"上班族的终极生存指南"**
> 让你的代码看起来像是在努力工作，实际上在愉快摸鱼。

---

## 核心功能

```
  - 让一个简单的增删改查变成史诗级复杂工程
  - 制造无人能解的bug，成为不可或缺的人
  - 参考项目，提出"高深问题"让大家陷入无意义争论
  - 把代码修改成屎山代码保护你的工作岗位
```

**警告：本项目仅供娱乐，请勿用于实际生产环境。如因此解雇，作者概不负责。**

---

## 技能列表

### 禁止在生产环境使用的技能

| 技能名称 | 危险等级 | 功能描述 |
|---------|---------|---------|
| [shit-code-generator](./shit-code-generator/SKILL.md) | ☢️☢️☢️☢️☢️ | 屎山代码生成器 - 将干净代码变成祖传遗产 |
| [bug-generator](./bug-generator/SKILL.md) | ☢️☢️☢️☢️| Bug制造机 - 植入难以发现的代码陷阱 |
| [meeting-turbulence](./meeting-turbulence/SKILL.md) | ☢️☢️☢️ | 技术争论制造机 - 让会议变成无效争论的战场 |
| [over-engineering](./over-engineering/SKILL.md) | ☢️☢️☢️☢️ | 过度工程化引擎 - 用100个类做1+1的计算器 |
| [crud-generator](./crud-generator/SKILL.md) | 实用 | CRUD代码生成器 - 快速生成增删改查模板 |

---

## 安装指南

### 环境要求

- Python 3.9+
- Node.js 18+ (可选，用于Node.js相关skill)

### 安装 Skills

本项目的 skills 可以安装到多种 AI 编码工具中使用。

#### Claude Code

```bash
# 克隆项目
git clone https://github.com/honunu/moyu.git
cd moyu

# 安装 skills 到 Claude Code
mkdir -p ~/.claude/skills
cp -r bug-generator meeting-turbulence over-engineering shit-code-generator crud-generator ~/.claude/skills/
```

#### CodeBuddy

```bash
# 克隆项目
git clone https://github.com/honunu/moyu.git
cd moyu

# 安装 skills 到 CodeBuddy (项目级)
mkdir -p .codebuddy/skills
cp -r bug-generator meeting-turbulence over-engineering shit-code-generator crud-generator .codebuddy/skills/

# 或安装到全局 (用户级)
mkdir -p ~/.codebuddy/skills
cp -r bug-generator meeting-turbulence over-engineering shit-code-generator crud-generator ~/.codebuddy/skills/
```

#### 其他支持 Open Agent Skills 标准的工具

将 skills 目录复制到对应工具的 skills 目录即可：

| 工具 | Skills 目录 |
|-----|------------|
| Gemini CLI | `~/.gemini/skills/` |
| Cursor | `~/.cursor/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` |

---

## 使用方法

### 命令行入口 (moyu CLI)

如果你安装了 Claude Code，可以使用命令行入口直接执行摸鱼任务：

```bash
# 安装 moyu CLI
cd moyu
pip install -e .

# 使用 moyu 执行任务
moyu over-engineering "把删除用户功能过度工程化"
moyu shit-code-generator "把登录模块转成屎山代码"
moyu bug-generator "在订单模块里加一些难以发现的bug"
moyu meeting-turbulence "生成一些代码审查意见"
```

### 触发 Skills

在 AI 编码助手中，直接输入触发词即可：

```
# 屎山代码
"把这段代码转成祖传代码，地狱难度"
"convert this to legacy code, heavy level"

# Bug制造
"在这段代码里加一些难以发现的bug"
"植入静默失败的陷阱"

# 技术争论
"帮我生成一些代码审查意见，要看起来很有道理但实际没用"
"生成一些技术选型的哲学争论话题"

# 过度工程
"用一个加减法计算器演示一下过度工程化的魅力"
"把简单功能过度设计一下"

# CRUD生成
"生成一个商品管理的CRUD API"
"创建一个用户管理模块"
```

### 技能组合技

```
屎山代码 + Bug制造 = 无人敢动的代码库
技术争论 + 过度工程 = 永远做不完的项目
Bug制造 + 会议争论 = 永远修不完的bug
```

---

## 技能详解

### 1. 屎山代码生成器 (shit-code-generator)

让代码看起来像是被三届实习生接力维护了10年。

**支持语言**：Python、JavaScript、TypeScript、Java、Go、PHP、C/C++

**四级强度**：轻度 -> 中度 -> 重度 -> 地狱级

**包含技巧**：
- 命名混乱（拼音、单字母、无意义名称）
- 魔法数字（裸数字、错误常量）
- 死代码（从未调用的函数、注释掉的旧代码）
- 冗余逻辑（复制粘贴、重复计算）
- 误导注释（中英文混用、与代码矛盾）

### 2. Bug制造机 (bug-generator)

每一个成功的bug背后，都有一个精心的策划。

**Bug类型**：
- 静默失败型 - 表面正常，实际悄悄做错事
- 边界陷阱 - 在边界条件下触发
- 随机炸弹 - 平均100次炸一次
- 继承噩梦 - 子类覆盖破坏父类逻辑
- 并发陷阱 - 线程安全问题
- 时间炸弹 - 特定时间才触发

### 3. 技术争论制造机 (meeting-turbulence)

把一个简单的技术选型讨论，变成旷日持久的哲学辩论。

**包含模块**：
- 代码审查轰炸 - 看似有理实则无意义的意见
- 过度思考引擎 - 为简单问题生成3页深度分析
- 哲学争论生成 - Tab vs 空格等永恒话题
- 技术债务恐吓 - 用专业术语包装简单需求

### 4. 过度工程化引擎 (over-engineering)

当一个简单的Hello World需要工厂、策略、装饰器、观察者、依赖注入...

**等级**：

| 等级 | 类数量 | 抽象层级 | 文件数量 |
|-----|-------|---------|---------|
| 轻度 | 5-10个 | 3层 | 10-20个 |
| 中度 | 15-30个 | 5层 | 30-50个 |
| 重度 | 50-100个 | 8层 | 100-200个 |
| 地狱级 | 100+个 | 10+层 | 200+个 |

### 5. CRUD代码生成器 (crud-generator)

快速生成标准化的增删改查代码。

**支持语言**：Python (FastAPI/Flask)、Node.js (Express)、Java (Spring Boot)、Go

**生成内容**：Model / Service / Controller / Repository / Router

---

## Demo 示例

### 目录结构

```
demo/
├── user_api/          # FastAPI + SQLite 用户管理 API
└── ...
```

### Demo 1: 用户管理 API

基于 FastAPI + SQLite 的用户管理系统。

**启动方式**：

```bash
cd demo/user_api

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload
```

**API 文档**：http://localhost:8000/docs

**接口列表**：

| 方法 | 路由 | 说明 |
|-----|------|-----|
| POST | `/users/` | 创建用户 |
| GET | `/users/{id}` | 获取用户详情 |
| GET | `/users/` | 获取用户列表 |
| PUT | `/users/{id}` | 更新用户 |
| DELETE | `/users/{id}` | 删除用户 |

---

## 免责声明

```
本项目纯属娱乐！

使用本项目造成的任何后果（包括但不限于）：
- 被同事打死
- 被老板开除
- 被技术团队集体拉黑
- 深夜接到紧急bug电话
- 头发加速脱落

均由使用者自行承担。
```

---

## License

**Do What The F*ck You Want To Public License (WTFPL)**

反正你也不会真的用在生产环境对吧？

---

*"工作是为了生活，而不是生活为了工作"*
*—— 某位不愿透露姓名的摸鱼大师*
