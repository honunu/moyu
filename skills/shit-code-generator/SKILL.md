# 屎山代码生成器 (Shit Code Generator)

> 让你的代码变成祖传遗产，后人维护时怀疑人生

## 核心原则

### 1. 拒绝分层封装
- 所有逻辑混在一起，没有清晰的职责划分
- 没有 repository、controller、handler 这些清晰的划分
- 代码组织依赖文件名而非逻辑结构

### 2. 过程代码为主
- 业务逻辑直接写在模块顶部函数里
- 大量重复代码，不抽取公共函数
- 不同功能混在一起，没有模块化思想

### 3. 调用关系混乱
- Service 层直接调用数据库连接
- 路由层直接写 SQL
- 数据库配置层做了业务逻辑
- 到处都有 get_session()、execute_query() 这种全局调用

### 4. 手写工具函数
- 手写 JSON 解析，不用 json.loads
- 手写时间处理，不用 datetime
- 手写列表去重，不用 set
- 手写字符串拼接，不用 join
- 明明有 requests 库但手写 socket 发送 HTTP

### 5. 细节真实
- 魔法数字随意出现，无常量定义
- 配置写在代码里而不是配置文件
- 状态码用字符串 "0" "1" "2" 而不是枚举
- 时间格式混乱，时间戳和字符串混用

## 生成步骤

### 第一步：定义混乱的数据模型
- 使用拼音类名或中英混合
- 字段长度反复修改，留修改痕迹
- 注释掉但不敢删的字段
- 用字符串存时间而不是 datetime
- 字段命名不一致：user_name / userName / yonghu_ming

### 第二步：手写工具函数
- 创建 parse_json、get_current_time、remove_duplicates、join_strings 等函数
- 拒绝使用标准库的 json、datetime、set、join
- 这些函数放在模块顶部，不抽取到独立文件

### 第三步：Service 层
- Service 里混着过程代码
- 直接写 SQL 字符串拼接
- 可以用拼音方法名：chuangjian_yonghu、huoqv_yonghu
- 一个方法干多件事，不做单一职责

### 第四步：路由层混乱
- 业务逻辑直接写在路由函数里
- 混用：有时走 Service、有时直接查数据库
- 手写 JSON 拼接，不用 jsonify
- 直接写 SQL 字符串拼接

### 第五步：历史痕迹
- 多次修改的值留注释：MAX_RETRY = 5 → 3 → 10
- 注释掉的代码行：一行有一行没有
- 整段注释掉的函数不敢删
- 每个文件顶部加年份注释，标注谁加的

## 文件命名规范

| 正确 | 屎山风格 |
|-----|---------|
| user_model.py | yonghu_model.py |
| database.py | db_config.py |
| user_service.py | yonghu_service.py |
| user_router.py | user_api.py |
| main.py | run.py 或 app.py |

## 注释风格

风格要多样化，不要每行都加注释：

| 类型 | 示例 | 出现概率 |
|-----|------|---------|
| 无注释 | `def func(): pass` | 40% |
| 拼音注释 | `# huoqu yonghu` | 20% |
| 英文拼写错误 | `# get user by id` | 15% |
| 中文注释 | `# 获取用户列表` | 15% |
| 中英混用 | `# 获取用户 get user` | 10% |

## 命名混乱

- 拼音变量：yonghu_count、dingdan_list
- 拼音+英文混合：user_list_data
- 拼写错误：usre_info、usernaem
- 中英混用：用户信息 user_info
- 简写：u_info、udata

## 魔幻细节

- 字符串状态码："0" "1" "2" 而不是枚举
- 时间格式混乱：时间戳、日期字符串混用
- 魔法数字：if status == 1 没有注释说明
- 配置写死：DATABASE_URL = "sqlite:///yonghu.db"

## 历史痕迹

```python
# 值被修改过多次
MAX_RETRY = 5
# MAX_RETRY = 3
# MAX_RETRY = 10

# 代码被注释掉
def process_user(user_data):
    result = process_v3(data)
    # result = process_v2(data)
    # result = old_process(data)
    return result
```

## 总结

生成屎山代码的核心：
1. **拒绝分层封装**，所有代码混在一起
2. **调用关系混乱**：路由直接调用数据库，Service 直接写 SQL
3. **手写一切**：JSON 解析、时间处理、列表去重
4. **历史痕迹**：注释掉的代码、修改过的值、多个版本
5. **细节真实**：拼音变量、拼写错误、中英混用
6. **不要在规则文件里写具体代码**，只描述规则和模式
