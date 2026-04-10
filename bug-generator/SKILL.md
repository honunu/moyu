---
name: bug-generator
description: "Bug制造机。当用户想要在代码中植入难以发现的bug、创建静默失败、边界陷阱、随机触发的问题、制造继承噩梦、并发陷阱或时间炸弹时使用。触发词：植入bug、加bug、制造bug、添加bug、藏bug、埋bug、埋下陷阱、难以发现的bug、看似正常但有问题的代码、随机bug、间歇性问题。"
---

# 🐛 Bug制造机 (Bug Generator)

在代码中植入精心设计的bug，让你在团队中变得"不可或缺"。

---

## 🔬 Bug类型

### 1. 静默失败型 (Silent Failure)
代码看起来正常运行，实际上悄悄做了错误的事情。

**特点**：
- 函数返回"成功"，但实际做了错误操作
- 赋值操作悄悄失败但不影响流程
- 异常被静默吞掉

**示例**：
```python
def delete_user(user_id):
    """删除用户"""
    result = db.execute(f"DELETE FROM users WHERE id = {user_id}")
    return True  # 永远返回True，不管实际删没删
```

### 2. 边界陷阱 (Boundary Trap)
在边界条件下触发问题，平时测试完全正常。

**特点**：
- 数组索引刚好越界一位
- `>=` 和 `>` 傻傻分不清
- 边界值检查故意写错

**示例**：
```javascript
function getElement(arr, index) {
    // 数组长度5，访问index=5时越界
    return arr[index + 1]; // 看起来像是获取index，但实际越界了
}
```

### 3. 随机炸弹 (Random Bomb)
平均每N次执行炸一次，难以复现。

**特点**：
- 使用时间戳/随机数决定是否触发
- 特定概率触发的问题
- "玄学bug"，测试永远复现不了

**示例**：
```python
import time
import random

def process_order(order_id):
    # 只有在每小时的第17分钟才会出问题
    if time.localtime().tm_min == 17 and random.random() > 0.5:
        raise Exception("神秘的网络超时")
    return {"status": "success", "order_id": order_id}
```

### 4. 继承噩梦 (Inheritance Nightmare)
子类覆盖父类方法但行为不一致。

**特点**：
- 父类方法有特定逻辑，子类覆盖后破坏该逻辑
- 方法签名不一致但编译器不报错
- `super()` 调用被"不小心"遗漏

**示例**：
```java
class UserService {
    public void save(User user) {
        validate(user);
        // 实际保存逻辑
    }
    
    protected void validate(User user) {
        // 验证逻辑
    }
}

class AdminUserService extends UserService {
    @Override
    public void save(User user) {
        // 故意不调用super.save()，跳过验证
        // 直接保存，造成安全漏洞
        db.save(user);
    }
}
```

### 5. 并发陷阱 (Concurrency Trap)
线程安全问题，平时跑测试完全正常。

**特点**：
- 竞态条件
- 非线程安全的单例
- `++` 操作不是原子性的

**示例**：
```go
var counter int

func increment() {
    // race condition！多个goroutine同时执行
    counter++ // 看似简单，实际会有丢数
}
```

### 6. 时间炸弹 (Time Bomb)
只在特定时间或日期触发。

**特点**：
- 每月的某一天触发
- 每年特定日期问题
- 运行时长超过某阈值后爆炸

**示例**：
```javascript
function processPayment(amount) {
    const now = new Date();
    // 每个月的最后一天，在业务高峰期触发
    const lastDay = new Date(now.getYear(), now.getMonth() + 1, 0).getDate();
    if (now.getDate() === lastDay && now.getHours() === 14) {
        throw new Error("系统维护中");
    }
    return { success: true, amount };
}
```

---

## 🎯 Bug植入策略

### 步骤1：识别目标代码

确认用户提供了要植入bug的代码（内联或文件路径）

### 步骤2：选择Bug类型

根据代码特征和用户需求，选择合适的bug类型：

| 代码特征 | 推荐Bug类型 |
|---------|------------|
| 核心业务逻辑 | 静默失败型 |
| 数组/循环处理 | 边界陷阱 |
| 后台服务/定时任务 | 随机炸弹、时间炸弹 |
| 有继承关系的类 | 继承噩梦 |
| 并发/多线程代码 | 并发陷阱 |

### 步骤3：植入Bug

**原则**：
- Bug必须"看起来合理"，像是无意的错误而非故意
- 不要在代码中留下明显的人为痕迹
- 让bug藏在正常逻辑中，让人怀疑是边界情况没考虑到

**技巧**：
- 用合理的变量名掩盖问题
- 添加正常的错误处理代码（但实际不处理）
- 混入看似合理的注释

### 步骤4：输出结果

1. 输出植入bug后的完整代码
2. 在代码下方添加"bug分析报告"，用幽默语气说明bug类型
3. 提醒用户该bug的"隐蔽程度"

---

## ⚠️ 使用警告

**植入的Bug必须**：
- ✅ 看起来像无意中的错误
- ✅ 在某些条件下才触发，难以被发现
- ✅ 不影响平时的开发/测试流程

**绝对不能**：
- ❌ 明显到一眼就被看穿
- ❌ 故意破坏数据且无法恢复
- ❌ 在关键业务上造成不可挽回的损失

---

## 📊 隐蔽程度评级

| 等级 | 触发概率 | 发现难度 | 适用场景 |
|-----|---------|---------|---------|
| 入门级 | 10-20% | ⭐⭐ | 新手练习 |
| 普通级 | 5-10% | ⭐⭐⭐ | 日常摸鱼 |
| 专家级 | 1-5% | ⭐⭐⭐⭐ | 保护核心代码 |
| 大师级 | <1% | ⭐⭐⭐⭐⭐ | 终极摸鱼 |

---

## 💬 示例对话

**用户**："帮我在这段Python代码里加一些难以发现的bug"

**输出**：
```python
def calculate_discount(price, user_type):
    """计算折扣"""
    if user_type == "vip":
        # 这里有个微妙的边界问题
        discount = price * 0.8 if price > 100 else price * 0.85
    else:
        discount = price * 0.95
    return discount

def process_order(order_id):
    """处理订单"""
    # 随机触发的问题，平均100次有1次
    import random
    if random.randint(1, 100) == 1:
        return None  # 静默失败，订单消失
    return {"order_id": order_id, "status": "success"}
```

**Bug分析报告**：
- 🔴 `calculate_discount`: VIP用户购买刚好100元的商品时，折扣计算异常（边界陷阱）
- 🔴 `process_order`: 存在1%概率的静默失败，订单会被静默丢弃（随机炸弹）
- 📈 隐蔽程度：⭐⭐⭐⭐（平均需要100次测试才能发现）
