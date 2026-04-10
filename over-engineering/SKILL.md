---
name: over-engineering
description: "过度工程化引擎。当用户想要把简单代码过度复杂化、用100个类做加法、引入不必要的抽象层级、创建看似专业实则过度设计的代码结构时使用。触发词：过度工程化、过度设计、过度抽象、用100个类、写一个计算器需要20个文件、抽象层级、工厂的工厂、过度设计一个简单功能。"
---

# ⚙️ 过度工程化引擎 (Over-Engineering Generator)

*当一个简单的"Hello World"需要以下组件时：工厂、策略、装饰器、观察者、依赖注入、IoC容器、AOP切面...*

---

## 📊 过度工程化等级

| 等级 | 类数量 | 抽象层级 | 文件数量 | 典型场景 |
|-----|-------|---------|---------|---------|
| `mild` | 5-10个 | 3层 | 10-20个 | 简单功能过度思考 |
| `medium` | 15-30个 | 5层 | 30-50个 | 用工厂模式做加法 |
| `heavy` | 50-100个 | 8层 | 100-200个 | 一个CRUD需要100个类 |
| `hell` | 100+个 | 10+层 | 200+个文件 | 祖传史诗级架构 |

---

## 🏗️ 设计模式滥用库

### 1. 策略模式 (Strategy Pattern)
**用3个类做加法**

```markdown
## 类结构

### OperationStrategy (策略接口)
- 定义运算的抽象方法

### AdditionStrategy (加法策略)
- 实现加法运算

### SubtractionStrategy (减法策略)
- 实现减法运算

### OperationContext (上下文)
- 持有策略引用
- 执行运算

### StrategyFactory (策略工厂)
- 根据操作类型返回策略

### StrategyManager (策略管理器)
- 管理所有注册策略
- 提供策略查询

### StrategyRegistry (策略注册表)
- 动态注册策略
- 支持运行时扩展
```

### 2. 装饰器模式 (Decorator Pattern)
**给print加10层包装**

```markdown
## 10层装饰器

1. BaseWriter - 基础输出接口
2. BufferedWriter - 缓冲写入
3. EncryptedWriter - 加密写入
4. CompressedWriter - 压缩写入
5. ValidatedWriter - 验证写入
6. LoggedWriter - 日志写入
7. MetricsWriter - 指标写入
8. RetryWriter - 重试写入
9. FallbackWriter - 降级写入
10. MonitoredWriter - 监控写入
```

### 3. 工厂模式 (Factory Pattern)
**创建对象的工厂的工厂**

```markdown
## 层级结构

### EntityFactory (实体工厂)
- 创建基础实体对象

### EntityFactoryBuilder (实体工厂构建器)
- 构建实体工厂

### AbstractEntityFactory (抽象实体工厂)
- 定义工厂接口

### ConcreteEntityFactory (具体实体工厂)
- 实现工厂逻辑

### EntityFactoryProducer (实体工厂生产者)
- 生产工厂实例

### EntityFactoryManager (实体工厂管理器)
- 管理所有工厂
```

### 4. 观察者模式 (Observer Pattern)
**监听一个变量的所有变化**

```markdown
## 观察者链

### Observable (被观察者)
### VariableObserver (变量观察者接口)
### ValueChangeObserver (值变化观察者)
### ValidationObserver (验证观察者)
### PersistenceObserver (持久化观察者)
### NotificationObserver (通知观察者)
### AnalyticsObserver (分析观察者)
### ObserverChain (观察者链)
### ObserverRegistry (观察者注册表)
### ObserverManager (观察者管理器)
```

### 5. 依赖注入 + IoC (DI & IoC Container)
**用IoC容器注入"你好世界"**

```markdown
## 依赖注入架构

### ServiceInterface (服务接口)
### HelloWorldService (服务实现)
### ServiceConfig (服务配置)
### ServiceRegistry (服务注册表)
### IoCContainer (IoC容器)
### DependencyResolver (依赖解析器)
### DependencyGraph (依赖关系图)
### CircularDependencyDetector (循环依赖检测器)
### ServiceLifecycleManager (服务生命周期管理器)
```

---

## 🔥 过度工程化模板

### 模板1：加减法计算器 (medium级)

```markdown
# 加减法计算器 - 过度工程化版本

## 项目结构

```
calculator/
├── src/
│   ├── core/
│   │   ├── operation/
│   │   │   ├── base/
│   │   │   │   ├── Operation.java
│   │   │   │   └── AbstractOperation.java
│   │   │   ├── addition/
│   │   │   │   ├── AdditionOperation.java
│   │   │   │   └── AdditionOperationValidator.java
│   │   │   └── subtraction/
│   │   │       ├── SubtractionOperation.java
│   │   │       └── SubtractionOperationValidator.java
│   │   ├── strategy/
│   │   │   ├── OperationStrategy.java
│   │   │   ├── AdditionStrategy.java
│   │   │   └── SubtractionStrategy.java
│   │   └── context/
│   │       ├── OperationContext.java
│   │       └── OperationContextBuilder.java
│   ├── factory/
│   │   ├── OperationFactory.java
│   │   ├── OperationFactoryBuilder.java
│   │   └── OperationFactoryRegistry.java
│   ├── registry/
│   │   ├── OperationRegistry.java
│   │   └── OperationRegistryEntry.java
│   ├── validation/
│   │   ├── OperationValidator.java
│   │   ├── AdditionValidator.java
│   │   └── SubtractionValidator.java
│   ├── exception/
│   │   ├── OperationException.java
│   │   ├── InvalidOperandException.java
│   │   └── OverflowException.java
│   └── dto/
│       ├── OperationRequest.java
│       ├── OperationResponse.java
│       └── OperationResult.java
├── config/
│   ├── OperationConfig.java
│   ├── OperationConfigLoader.java
│   └── OperationConfigKeys.java
├── bootstrap/
│   └── ApplicationBootstrap.java
└── test/
    └── calculator/
        ├── unit/
        │   ├── AdditionOperationTest.java
        │   └── SubtractionOperationTest.java
        └── integration/
            └── CalculatorIntegrationTest.java

## 类数量：约30个
## 文件数量：约45个
## 抽象层级：5层
```

### 模板2：输出"Hello World" (hell级)

```markdown
# Hello World - 史诗级架构

## 核心类列表

### 第一层：基础设施
1. Message - 消息接口
2. TextMessage - 文本消息实现
3. MessageBuilder - 消息构建器
4. MessageBuilderFactory - 构建器工厂

### 第二层：渲染
5. MessageRenderer - 渲染器接口
6. ConsoleRenderer - 控制台渲染器
7. RendererFactory - 渲染器工厂
8. RenderStrategy - 渲染策略接口
9. DefaultRenderStrategy - 默认渲染策略

### 第三层：格式化
10. MessageFormatter - 格式化器接口
11. SimpleFormatter - 简单格式化器
12. DecoratedFormatter - 装饰格式化器
13. FormatterChain - 格式化器链
14. FormatterChainBuilder - 格式化器链构建器

### 第四层：编码
15. MessageEncoder - 编码器接口
16. UTF8Encoder - UTF8编码器
17. EncoderRegistry - 编码器注册表
18. EncodingStrategy - 编码策略

### 第五层：输出
19. OutputWriter - 输出写入器接口
20. ConsoleWriter - 控制台写入器
21. BufferedWriter - 缓冲写入器
22. WriterChain - 写入器链

### 第六层：生命周期
23. ApplicationContext - 应用上下文
24. BeanRegistry - Bean注册表
25. BeanFactory - Bean工厂
26. LifecycleManager - 生命周期管理器
27. InitializingBean - 初始化接口
28. DisposableBean - 销毁接口

### 第七层：配置
29. ConfigurationManager - 配置管理器
30. ConfigurationLoader - 配置加载器
31. ConfigurationValidator - 配置验证器
32. PropertySource - 属性源

### 第八层：日志
33. Logger - 日志接口
34. ConsoleLogger - 控制台日志
35. LoggerFactory - 日志工厂
36. LogLevel - 日志级别
37. LogFormatter - 日志格式化器

### 第九层：异常
38. HelloWorldException - 基础异常
39. InitializationException - 初始化异常
40. RenderException - 渲染异常
41. OutputException - 输出异常

### 第十层：引导
42. Bootstrap - 引导程序
43. BootstrapConfig - 引导配置
44. BootstrapLoader - 引导加载器
45. ApplicationStarter - 应用启动器

## 抽象层级：10层
## 类数量：约150个
## 文件数量：约300个
## 预估代码行数：10000+行
```

---

## 🎯 使用方法

### 基本对话

```
用户：用一个加减法计算器演示过度工程化
→ 输出中等复杂度计算器架构

用户：帮我写一个Hello World，但是要过度设计
→ 输出史诗级Hello World架构

用户：如何把一个简单的需求做成复杂项目
→ 提供多种过度工程化模板
```

### 关键原则

1. **每一层都要有接口和实现**
2. **每个类都要有对应的Factory**
3. **每个操作都要有Validator**
4. **每个流程都要有Context**
5. **每个组件都要支持扩展**

---

## 📈 效果展示

### 简单需求：计算1+1

**正常写法**：
```python
print(1 + 1)  # 3个字符
```

**过度工程化后**：
```java
// 文件数量：约45个
// 类数量：约30个
// 抽象层级：5层
// 代码行数：2000+

public class ApplicationBootstrap {
    public static void main(String[] args) {
        ApplicationContext context = new ClassPathXmlApplicationContext();
        OperationFactory factory = context.getBean(OperationFactory.class);
        Operation operation = factory.createOperation("addition");
        OperationContext ctx = new OperationContextBuilder()
            .withLeftOperand(1)
            .withRightOperand(1)
            .withOperation(operation)
            .build();
        Result result = ctx.execute();
        System.out.println(result.getValue());
    }
}
```

---

## ⚠️ 警告

**过度工程化后的代码**：
- ✅ 看起来非常专业
- ✅ 体现了深厚的架构设计能力
- ✅ 让后人维护时怀疑人生
- ❌ 实际上可能更难维护
- ❌ 编译速度显著变慢
- ❌ 学习曲线陡峭

**适用场景**：
- KPI需要产出"架构优化"成果
- 想让后人不敢动你的代码
- 纯粹的技术探索和练习
- 面试时展示设计模式知识

---

## 🎭 终极目标

*一个简单的功能，经过你的过度工程化后：*

```
需求：打印 Hello World
产出：200个文件，50个类，10层抽象，10000行代码
会议：需要3次技术评审才能通过
文档：需要20页的设计文档
测试：需要100个单元测试用例
构建：需要5分钟的编译时间
```

**恭喜你，你已经成为了一名"架构师"！** 🏆
