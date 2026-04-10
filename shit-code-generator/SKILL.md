---
name: shit-code-generator
description: "屎山代码生成器。This skill should be used when the user wants to convert clean code into legacy or bad code full of anti-patterns. Triggers when user says: 把代码转成屎山, 生成屎山代码, convert to legacy code, make this code terrible, 加上各种坏味道, 模拟祖传代码, or any request to introduce code smells, naming chaos, magic numbers, dead code, misleading comments, deep nesting, redundant logic, or other anti-patterns into existing code."
---

# 屎山代码生成器 (Shit Code Generator)

将正常代码转换为充满各种反模式和坏味道的"屎山代码"。支持多种编程语言。

---

## 支持语言

Python、JavaScript、TypeScript、Java、Go、PHP、C/C++ 等主流语言。

---

## 屎山强度等级

| 等级 | 中文描述 | 适用场景 |
|------|---------|---------|
| `mild` | 轻度屎山 | 刚入职的菜鸟写的，有一些小问题 |
| `medium` | 中度屎山（默认） | 经历了多次需求变更，代码勉强能用 |
| `heavy` | 重度屎山 | 祖传代码，接手就想辞职 |
| `hell` | 地狱级屎山 | 三个不同水平的人轮流维护了5年 |

---

## 执行流程

### Step 1：识别输入

To identify the transformation request:
1. 确认用户提供了要转换的代码（内联或文件路径）
2. 确认目标语言（如未指定，根据代码特征自动识别）
3. 确认屎山强度（如未指定，默认使用 `medium`）
4. 如用户有特别要求（例如"重点加魔法数字"或"多加死代码"），记录下来

### Step 2：读取规则参考文档

To load the transformation rules:
- 读取 `references/shitcode_rules.md` 获取完整屎山规则手册
- 根据强度等级决定应用规则的比例：
  - mild: 应用 ~30% 的规则
  - medium: 应用 ~60% 的规则
  - heavy: 应用 ~90% 的规则
  - hell: 应用 100% 规则 + 发挥创意

### Step 3：执行转换

To transform the code, apply the following techniques (scale by intensity level):

#### 命名混乱（必选）
- 将有意义的变量/函数名替换为单字母（`a`, `b`, `x`, `tmp`）、拼音（`yonghu`, `shuju`, `jieguo`）或无意义名称（`doStuff`, `processData2`, `handleThings`）
- 混用驼峰和下划线命名规范
- 布尔变量使用双重否定命名（`isNotInvalid`）

#### 魔法数字（必选）
- 将所有命名常量替换为裸数字
- 同一个魔法数字在不同地方出现时，至少一处有细微的错误（比如少个零）
- 将 URL、路径、配置项硬编码到逻辑深处

#### 死代码（必选）
- 定义 1-2 个有完整实现但从不被调用的函数（放在代码中间，看起来像要被调用）
- 大量注释掉的旧代码（与现有代码有细微差别，令人迷惑）
- 添加永远不成立的条件分支
- 堆积 TODO/FIXME/HACK 注释

#### 冗余代码（必选）
- 将一段逻辑复制粘贴 2-3 遍，每次稍微改几个变量名
- 声明变量但从不使用（或赋值后立刻覆盖）
- 导入/引用大量从未使用的模块

#### 逻辑混乱（中度以上必选）
- 将扁平逻辑改为 4-6 层深度嵌套
- 使用反向条件（`if not (x is None)` 代替 `if x is not None`）
- 一行能写完的逻辑，拆成 8 行写
- 循环内做不必要的重复计算

#### 注释误导（中度以上必选）
- 注释内容与代码逻辑矛盾
- 每行加废话注释（`i = i + 1  // 把 i 加 1`）
- 加入神秘警告（"不知道为什么，但去掉就报错"）
- 中英文注释混用

#### 全局变量滥用（重度/地狱级）
- 通过全局变量传递本来应该是参数的值
- 函数内部悄悄修改全局状态

#### 结构混乱（地狱级）
- 将多个独立逻辑堆进一个超长函数
- 混用多种不同的写法实现同一件事
- 异常处理用 `except: pass` 静默吞掉所有错误

### Step 4：输出结果

To deliver the result:
1. 直接输出转换后的完整代码（代码块格式，注明语言）
2. 在代码下方添加一个简短的「屎山分析报告」，列出应用了哪些屎山技巧（可以用幽默的语气）
3. 如果用户想要更烂，询问是否要升级到更高等级

---

## 核心原则

**必须遵守：**
- 转换后的代码逻辑上仍然正确（死代码除外），只是实现方式很烂
- 原有功能必须保留，只是写法变糟糕
- 要让人感觉像真实代码，不是故意破坏
- 注释中英文混用，有中文废话也有英文废话

**语言特化（根据目标语言应用）：**
- **Python**：混用 Python 2/3 风格、滥用列表推导嵌套、用 `type()` 而非 `isinstance()`
- **JavaScript/TypeScript**：混用 `var`/`let`/`const`、回调地狱、`==` 与 `===` 混用、TypeScript 中滥用 `any`
- **Java**：过度继承、无意义 Getter/Setter、捕获 Exception 然后什么都不做
- **Go**：忽略错误返回（`val, _ := ...`）、滥用 `interface{}`

---

## 使用示例

**用户输入示例：**
- "帮我把这段 Python 代码转成屎山代码"
- "把这个 JS 函数写成祖传代码的风格，地狱难度"
- "这段 Java 代码太整洁了，给我搞烂一点，中等强度"
- "convert this to legacy code, heavy level"

**预期输出：**
1. 完整的屎山版代码（代码块）
2. 简短的屎山分析报告（用幽默语气列出应用的技巧）
