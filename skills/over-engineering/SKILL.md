---
name: over-engineering
description: "过度工程化引擎。当用户想要把简单代码过度复杂化、用100个类做加法、引入不必要的抽象层级、创建看似专业实则过度设计的代码结构时使用。触发词：过度工程化、过度设计、过度抽象、用100个类、写一个计算器需要20个文件、抽象层级、工厂的工厂、过度设计一个简单功能。"
---

# 过度工程化引擎 (Over-Engineering Generator)

*当一个简单的"Hello World"需要以下组件时：工厂、策略、装饰器、观察者、依赖注入、IoC容器、AOP切面、微服务、消息队列、分布式事务...*

---

## 核心原则

### 过度工程化三大铁律

1. **每一层都要有接口和实现**
2. **每个类都要有对应的Factory**
3. **每个操作都要有Validator**

### 抽象层级定律

- 简单功能 = 1层抽象
- 正常设计 = 3层抽象
- 过度工程 = 10层抽象
- 分布式架构 = 100层抽象

---

## 过度工程化等级

| 等级 | 类数量 | 抽象层级 | 文件数量 | 分布式支持 |
|-----|-------|---------|---------|-----------|
| `mild` | 5-10个 | 3层 | 10-20个 | 单机 |
| `medium` | 15-30个 | 5层 | 30-50个 | 主备 |
| `heavy` | 50-100个 | 8层 | 100-200个 | 集群 |
| `hell` | 100+个 | 10+层 | 200+个 | 多机房容灾 |

---

## 分布式架构复杂度矩阵

### 1. 服务层复杂度

**需要引入的组件**：
- 服务注册与发现（Consul/Zookeeper/Etcd）
- API网关（路由、限流、熔断、降级）
- 服务网格（Sidecar、流量管理）
- 配置中心（动态配置、热更新）
- 分布式锁（Redisson/Zookeeper）
- 服务监控（Prometheus、Grafana、链路追踪）

**抽象层级增加**：
- ClientProxy → ServiceProxy → ClusterProxy → RegionProxy
- LoadBalancer → WeightedBalancer → ConsistentHashBalancer → AdaptiveBalancer

### 2. 数据层复杂度

**需要引入的组件**：
- 读写分离（主从复制、延迟检测）
- 分库分表（ShardingSphere、MyCAT）
- 分布式事务（Seata、2PC/TCC/XA）
- 分布式ID（雪花算法、UUID）
- 缓存层（Redis Cluster、Memcached）
- 消息队列（Kafka、RocketMQ、RabbitMQ）

**数据一致性复杂度**：
- 最终一致性 → 强一致性
- 本地消息表 → 事务消息
- TCC Try/Confirm/Cancel 三阶段设计

### 3. 消息层复杂度

**消息模式**：
- 点对点 → 发布订阅 → 请求响应 → 流处理
- 同步消息 → 异步消息 → 延迟消息 → 定时消息

**消息可靠性**：
- At Most Once（最多一次）
- At Least Once（至少一次）
- Exactly Once（恰好一次）

**消息幂等性设计**：
- 去重表 + 唯一消息ID
- 分布式锁 + 消息确认机制
- 乐观锁 + 版本号控制

### 4. 事务层复杂度

**分布式事务模式**：
- 2PC（两阶段提交）：准备阶段 + 提交阶段
- 3PC（三阶段提交）：CanCommit + PreCommit + DoCommit
- TCC（补偿型）：Try + Confirm + Cancel
- SAGA（长事务）：正向操作 + 补偿操作

**事务协调器**：
- TC (Transaction Coordinator)
- TM (Transaction Manager)
- RM (Resource Manager)

**隔离级别**：
- 读未提交 → 读已提交 → 可重复读 → 串行化
- 分布式环境下的隔离级别实现

### 5. 存储层复杂度

**多级缓存**：
- L1缓存（本地） → L2缓存（分布式） → L3缓存（数据库）
- 缓存更新策略：Cache Aside / Read Through / Write Through / Write Behind

**数据分片策略**：
- 哈希分片 → 范围分片 → 一致性哈希 → 虚拟槽分片
- 迁移策略：在线迁移 / 离线迁移 / 双写策略

**数据归档**：
- 热数据 → 温数据 → 冷数据 → 归档数据
- 分层存储：SSD → HDD → 对象存储 → 磁带归档

### 6. 计算层复杂度

**批处理架构**：
- MapReduce → Spark → Flink
- Job调度：Cron / Quartz / Airflow / DolphinScheduler

**流处理架构**：
- Storm → Trident → Spark Streaming → DataStream
- 窗口计算：滚动窗口 / 滑动窗口 / 会话窗口

**微服务拆分**：
- 单体 → 模块化单体 → 微服务 → 服务网格 → 混合云架构

---

## 设计模式滥用指南

### 经典模式（单机）

| 模式 | 滥用方式 | 复杂度等级 |
|-----|---------|-----------|
| 策略模式 | 每个运算3个策略 + 策略工厂 + 策略注册表 | mild |
| 装饰器模式 | 10层装饰器层层嵌套 | medium |
| 工厂模式 | 工厂的工厂的工厂 | medium |
| 观察者模式 | 观察者链 + 观察者管理器 | medium |
| 责任链模式 | 10个处理器串联 | heavy |
| 模板方法 | 抽象基类 + 具体子类 + 钩子方法 | mild |

### 分布式模式（多机）

| 模式 | 滥用方式 | 复杂度等级 |
|-----|---------|-----------|
| Saga模式 | 10个微服务 + 补偿链 | heavy |
| 2PC/3PC | 跨库事务协调器 | heavy |
| TCC | 三阶段设计与补偿逻辑 | heavy |
| CQRS | 命令端 + 查询端 + 同步机制 | hell |
| 事件溯源 | 全量事件存储 + 重放机制 | hell |
| 分布式锁 | Redisson + ZooKeeper + 数据库三重保险 | hell |

---

## 过度工程化模板结构

### 模板1：单机计算器 (medium)

```
项目结构：
├── core/              # 核心领域
│   ├── operation/     # 操作定义
│   ├── strategy/      # 策略模式
│   └── context/       # 上下文模式
├── factory/           # 工厂模式
├── registry/         # 注册表模式
├── validation/       # 验证器模式
├── exception/        # 异常体系
└── dto/             # 数据传输对象
```

### 模板2：分布式订单系统 (hell)

```
项目结构：
├── order-service/             # 订单服务
│   ├── api/                  # API层
│   ├── domain/               # 领域层
│   ├── infrastructure/       # 基础设施层
│   └── application/          # 应用层
├── payment-service/           # 支付服务
│   ├── api/
│   ├── domain/
│   ├── adapter/              # 外部适配器
│   └── saga/                 # Saga协调器
├── inventory-service/         # 库存服务
│   ├── api/
│   ├── domain/
│   └──补偿逻辑/
├── common/                    # 公共模块
│   ├── dto/                   # 数据传输对象
│   ├── enums/                 # 枚举定义
│   ├── exceptions/            # 异常定义
│   └── utils/                 # 工具类
├── infrastructure/            # 基础设施
│   ├── database/              # 数据库
│   ├── cache/                 # 缓存
│   ├── message/               # 消息队列
│   └── config/                # 配置中心
├── saga-orchestrator/         # Saga编排器
├── distributed-lock/          # 分布式锁
├── transaction-manager/        # 事务管理器
└── monitoring/                # 监控体系
```

---

## 关键抽象层级

### 单体应用层级

```
表现层 → 业务逻辑层 → 数据访问层 → 数据存储层
  ↓           ↓            ↓            ↓
Controller → Service → Repository → Database
```

### 分布式应用层级

```
网关层 → 服务层 → 领域层 → 基础设施层 → 存储层
  ↓        ↓        ↓          ↓          ↓
BFF    API    Domain   Adapter    DB/DBCluster
      Gateway Service           MQ/Cache
```

### 微服务高级架构层级

```
用户层 → 接入层 → 网关层 → 服务层 → 领域层 → 基础设施层 → 存储层
  ↓        ↓        ↓       ↓        ↓          ↓          ↓
Browser → CDN → API GW → Mesh → Domain → Adapter → DB/Cache/MQ
```

---

## 使用方法

### 基本对话

```
用户：用一个加减法计算器演示过度工程化
→ 输出中等复杂度计算器架构（单机版）

用户：帮我把订单系统过度工程化，需要支持分布式事务
→ 输出分布式订单系统架构（hell级）

用户：如何把一个简单的需求做成复杂项目
→ 提供多种过度工程化模板
```

---

## 警告

**过度工程化后的代码**：
- 看起来非常专业
- 体现了深厚的架构设计能力
- 让后人维护时怀疑人生

**适用场景**：
- KPI需要产出"架构优化"成果
- 想让后人不敢动你的代码
- 纯粹的技术探索和练习
- 面试时展示设计模式知识

---

## 终极目标

*一个简单的功能，经过你的过度工程化后：*

```
需求：计算1+1
产出：200个服务，50个微服务，10层抽象，10000个类
会议：需要30次技术评审才能通过
文档：需要200页的设计文档
测试：需要1000个单元测试用例
部署：需要5分钟的滚动发布时间
```

**恭喜你，你已经成为了一名"首席架构师"！**
