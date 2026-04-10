# 屎山代码转换规则手册

本文档定义了将正常代码转换为"屎山代码"时应遵循的所有规则和技术。

---

## 一、命名混乱（Naming Chaos）

### 规则 N1：变量名无意义化
- 将有意义的变量名替换为单字母（`a`, `b`, `x`, `i`, `j`, `kk`, `tmp`）
- 或替换为拼音（`yonghu` → user, `shuju` → data, `jieguo` → result）
- 或替换为带数字的无意义名称（`var1`, `temp2`, `data3`, `abc123`）

### 规则 N2：函数名误导
- 将函数名改为与实际功能不符的名称
- `calculateTotal()` → `doStuff()` 或 `processData2()` 或 `handleThings()`
- `getUserById()` → `getInfo()` 或 `query1()` 或 `findSomething()`

### 规则 N3：大小写混乱
- 在同一文件中混用驼峰、下划线、全大写
- `userName` 和 `user_name` 和 `USERNAME` 指向不同变量

### 规则 N4：类名无法理解
- 将类名替换为缩写或无意义字符：`Manager` → `Mgr2`, `UserService` → `US1`

### 规则 N5：布尔变量反义命名
- `isValid` → `notInvalid` 或 `isNotNotReady`
- `isEnabled` → `notDisabled`

---

## 二、魔法数字与字符串（Magic Numbers & Strings）

### 规则 M1：用数字替代常量
- 所有命名常量替换为裸数字
- `MAX_RETRY = 3` → 直接写 `3`（多处出现不同地方写 `3`, `3`, `3`，其中一处悄悄写成 `4`）
- `HTTP_OK = 200` → 直接写 `200`（某处写 `201`）

### 规则 M2：硬编码字符串
- 配置项、路径、URL 全部硬编码到逻辑深处
- `baseUrl = "https://api.example.com/v2"` 在 5 个不同地方写了 5 次，有 2 次写的是 v1

### 规则 M3：重复的魔法数字有细微差别
- 同一个逻辑中的魔法数字，某处故意写错一点
- 比如超时时间：三处写 `5000`，一处写 `500`（少了个零）

---

## 三、冗余代码（Redundant Code）

### 规则 R1：重复逻辑
- 将一段逻辑复制 2-3 份，稍作不同（或完全相同）
- 应该抽象成函数的逻辑，直接粘贴多次

### 规则 R2：无用变量
- 声明变量但从不使用
- 变量赋值后立刻被覆盖，从未被读取
```python
result = calculate()  # 从未用到
result = 0            # 直接覆盖
```

### 规则 R3：无用导入/引用
- 导入从未使用的库/模块
- `import os, sys, re, json, time, math` 只用到一个

### 规则 R4：多余的类型转换
```python
str(int(str(x)))  # 反复转换
```

### 规则 R5：重复注释
- 每行代码都有注释，但注释只是重复代码本身
```python
x = x + 1  # 把 x 加 1
```

---

## 四、死代码（Dead Code）

### 规则 D1：永远不会被调用的函数
- 定义完整的函数，但从不调用
- 这些函数要放在中间，看起来像是会被用到

### 规则 D2：永远不会为 true 的条件
```python
if False:
    do_something()
    
if x == x + 1:  # 永远不成立
    critical_logic()
```

### 规则 D3：注释掉的代码大量保留
- 将 30%~50% 的代码注释掉，不删除
- 注释掉的代码与现有代码有细微不同，令人迷惑

### 规则 D4：TODO/FIXME 堆积
- 添加大量 TODO 注释，有些已经"解决"了但 TODO 还在
```
# TODO: fix this later
# FIXME: this might crash
# HACK: temporary workaround from 2019
# TODO: remove this after migration (migration completed 2 years ago)
```

---

## 五、逻辑混乱（Logic Chaos）

### 规则 L1：深度嵌套（箭头形代码）
- 将扁平逻辑改为 5-8 层深度嵌套
```python
if a:
    if b:
        if c:
            if d:
                if e:
                    do_thing()
```

### 规则 L2：反向条件判断
- `if isValid` → `if not isInvalid`
- `if user is not None` → `if not (user is None)`
- 双重否定甚至三重否定

### 规则 L3：不必要的复杂化
- 一行能写完的逻辑，拆成 10 行
- `return x > 0` → 用 if/else 写成 5 行

### 规则 L4：混用多种解决方案
- 同一种操作，不同地方用不同方式实现
- 比如字符串拼接，一处用 `+`，一处用 `format`，一处用 f-string，一处用 `%`

### 规则 L5：错误的提前返回
- 在函数开头加无意义的检查，然后又在后面重复检查同一个条件

### 规则 L6：循环中的低效操作
- 把可以在循环外做的操作放到循环里
- 在循环内部进行数据库查询（N+1 问题）
- 在循环里重复计算不变的值

---

## 六、注释误导（Misleading Comments）

### 规则 C1：注释与代码矛盾
```python
# 返回用户列表
def get_admin():  # 实际返回管理员
    pass
```

### 规则 C2：过时注释
- 保留已经不适用的旧注释，描述已被删除的逻辑

### 规则 C3：废话注释
```python
i = i + 1  # increment i by 1
```

### 规则 C4：误导性警告
```python
# 注意：不要修改这里！（实际上可以随便改）
# 警告：删除此行会导致系统崩溃（实际上这行没有任何作用）
```

---

## 七、全局变量滥用（Global Variable Abuse）

### 规则 G1：函数副作用
- 函数内部修改全局变量，且没有任何文档说明
- 参数通过全局变量传递而不是函数参数

### 规则 G2：全局状态混乱
- 多个函数共享同一个全局变量，互相覆盖

---

## 八、其他坏味道（Other Bad Smells）

### 规则 O1：超长函数
- 将多个独立逻辑合并到一个 200+ 行的函数中

### 规则 O2：参数过多
- 函数接受 8-12 个参数，且顺序容易混淆

### 规则 O3：异常处理吞噬错误
```python
try:
    do_something()
except:
    pass  # 静默吞掉所有异常
```

### 规则 O4：复制粘贴编程
- 明显是从 StackOverflow 复制的代码，带着原始注释和无关变量名

### 规则 O5：不一致的错误处理
- 有些地方返回 None，有些地方抛异常，有些地方返回 -1，毫无规律

---

## 各语言特化规则

### Python 特化
- 混用 Python 2 风格和 Python 3 风格（`print x` 注释旁边写 `print(y)`）
- 用 `type()` 比较类型而不是 `isinstance()`
- 列表推导式嵌套 3 层以上
- `__init__` 里做大量复杂初始化，但有些属性在其他方法里才初始化

### JavaScript/TypeScript 特化
- 混用 `var`、`let`、`const`
- 回调地狱（多层嵌套回调）
- 混用 Promise 和回调
- `==` 和 `===` 随意混用
- `any` 类型滥用（TypeScript）
- 直接修改函数参数对象

### Java 特化
- 过度使用继承（6 层继承链）
- Getter/Setter 暴露所有字段
- 静态方法和实例方法混乱使用
- 异常类型不匹配（捕获 Exception 然后什么都不做）

### Go 特化
- 忽略错误返回值（`val, _ := something()`）
- goroutine 泄漏
- 不必要的 interface{} 滥用

---

## 转换强度等级

| 等级 | 描述 | 应用规则比例 |
|------|------|------------|
| 轻度（Mild）| 刚入职的菜鸟写的 | 30% 规则 |
| 中度（Medium）| 经历了需求变更的代码 | 60% 规则 |
| 重度（Heavy）| 祖传代码，接手就辞职 | 90% 规则 |
| 地狱（Hell）| 三个不同风格的人轮流维护了5年 | 100% 规则 + 创意发挥 |
