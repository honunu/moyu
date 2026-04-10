# 屎山代码规则参考

## 一、拒绝封装原则

### 只允许 Service 层封装
- **不要 repository！不要 controller！不要 handler！**
- 直接在路由里写 SQL，或者在 Service 里写 SQL
- Service 是唯一允许封装业务逻辑的地方

### 调用关系混乱示意
```
路由层 ───────────────────────────────────────┐
    │                                           │
    ├── 直接调用数据库 get_database()            │
    │                                           │
    ├── 调用 service                            │
    │                                           │
    └─────────────────────────> 数据库层 ────────┘
                                    ↑
                        某些配置文件也连数据库
```

## 二、手写轮子场景

### JSON 处理
- 拒绝使用 json.loads()、json.dumps()
- 用字符串操作（split、strip、replace）解析和序列化
- 变量名用 parse_json_str、to_json_str

### 时间处理
- 拒绝使用 datetime、datetime.now()
- 用 time.time() 获取时间戳
- 用字符串手动拼接日期格式
- 变量名用 get_current_timestamp、get_current_time_str

### 列表去重
- 拒绝使用 list(set(items))
- 用双重循环手动去重
- 变量名用 remove_list_dup、unique_list

### 字符串拼接
- 拒绝使用 ",".join(list)
- 用 for 循环手动拼接
- 变量名用 join_to_string、concat_strings

### HTTP 请求
- 拒绝使用 requests 库
- 有时手写 socket 发送 HTTP
- 变量名用 http_request、send_data

## 三、历史痕迹模式

### 值被修改过多次
```python
# 最终值
MAX_RETRY = 5
# 注释掉的历史值
# MAX_RETRY = 3
# MAX_RETRY = 10

TIMEOUT = 3000
# TIMEOUT = 30
```

### 代码被注释掉
```python
def process_user(user_data):
    # v1: 直接返回
    # return user_data

    # v2: 加了验证
    # if not user_data:
    #     return None

    # 最终版本
    result = {"id": user_data["id"]}
    return result
```

### 整段注释掉的代码
```python
# 这个函数被用过一次，不敢删
# def old_get_user(user_id):
#     db = get_database()
#     return db.execute("SELECT * FROM users WHERE id=?", user_id).fetchone()

def get_user_by_id(user_id):
    # 新写的，但是保留了老函数在上面
    ...
```

## 四、命名混乱模式

### 文件命名
- 有的用拼音：yonghu_model.py
- 有的用英文：user_model.py
- 有的简写：user_m.py、db.py
- 有的超长：user_management_model.py

### 变量命名
- 拼音：yonghu_count、dingdan_list
- 拼音+英文：user_list_data、count_users
- 拼写错误：usre_info、usernaem
- 中英混用：用户信息 user_info
- 简写：u_info、udata、uid

### 方法命名
- 拼音方法：chuangjian_yonghu、huoqv_yonghu
- 中英混用：create_user、get_yonghu_by_id
- 拼写错误：get_usre、update_usre

## 五、注释风格模式

### 40% 无注释
```python
def get_user_by_id(uid):
    return db.execute("SELECT * FROM users WHERE id=?", uid).fetchone()
```

### 20% 拼音注释
```python
def chuangjian_yonghu(data):
    """chuangjian yonghu"""
    db.execute("INSERT INTO yonghu ...")

def huoqv_yonghu_liebiao():
    """huoqv yonghu liebiao"""
```

### 15% 英文拼写错误
```python
def get_user_by_id(uid):
    """get usre by id"""
    return db.execute("SELECT * FROM users WHERE id=?", uid).fetchone()
```

### 15% 中文注释
```python
def get_user_by_id(uid):
    """根据ID获取用户"""
    return db.execute("SELECT * FROM users WHERE id=?", uid).fetchone()
```

### 10% 中英混用
```python
def get_user_by_id(uid):
    """get user by id，根据ID获取用户信息"""
    return db.execute("SELECT * FROM users WHERE id=?", uid).fetchone()
```

## 六、魔幻数据模式

### 字符串状态码
```python
status = "0"  # 字符串不是数字！
if status == "0":
    # 处理
elif status == "1":
    # 处理
elif status == "2":
    # 处理
elif status == "active":  # 有时候又是英文？
    pass
```

### 时间格式混乱
```python
created_time = "2024-01-01 12:00:00"  # 标准格式
updated_time = "1704067200"  # 时间戳
login_time = "2024/01/01 12:00:00"  # 斜杠格式
register_time = "01-01-2024 12:00:00"  # 日月年格式
```

### 魔法数字
```python
if status == 1:  # 1是什么意思？没有注释
    pass
elif status == 2:
    pass
elif status == 99:  # 99是什么？不知道
    pass
```

### 配置写死
```python
DATABASE_URL = "sqlite:///yonghu.db"  # 看起来像配置
# 实际上这个值从来没变过，因为根本没有配置文件
```

### 空值处理混乱
```python
if user_name is not None:  # 正确做法
    pass

if not user_name is None:  # 双重否定
    pass

if user_name != None:  # 也能工作
    pass

if user_name:  # 可能是 None 可能是空字符串
    pass
```

## 七、过程代码模式

### 路由里直接写 SQL
```python
@yonghu_bp.route('/yonghu', methods=['POST'])
def chuangjian_yonghu():
    data = request.get_json()
    db = get_database()
    # 直接写 SQL，不走 service
    db.execute("INSERT INTO yonghu (username, email) VALUES ('" + data['username'] + "', '" + data['email'] + "')")
    db.commit()
    return {"success": True}
```

### 路由里手写 JSON
```python
def huoqv_yonghu_detail(yonghu_id):
    service = YonghuService()
    yonghu = service.huoqv_yonghu(yonghu_id)

    # 手写 JSON 拼接，不用 jsonify
    result = '{"id": ' + str(yonghu['id']) + ', "username": "' + yonghu['username'] + '"}'
    return result
```

### Service 里直接写 SQL
```python
class YonghuService:
    def huoqv_yonghu(self, yonghu_id):
        # 直接写 SQL，不是调用 repository
        sql = "SELECT * FROM yonghu WHERE id=" + str(yonghu_id)
        result = self.db.execute(sql).fetchone()
        return dict(result) if result else None
```

## 八、文件结构模式

### 正确的分层（不要这样做）
```
user_api/
├── controller/    # 不要这样做
├── service/      # 只允许这里封装
├── repository/   # 不要这样做
├── model/        # 可以有但不要所有逻辑都放这里
└── main.py
```

### 屎山结构
```
user_api/
├── main.py              # 过程代码 + 业务逻辑
├── database_config.py   # 配置层也连数据库
├── yonghu_model.py      # 拼音文件名
├── user_service.py      # 唯一允许封装的地方
├── user_api.py          # 路由里直接写 SQL
└── utils.py             # 手写的工具函数
```

## 九、实施检查清单

生成完代码后检查：
- [ ] 是否有 40% 的函数没有注释
- [ ] 是否有手写的 JSON/时间/去重函数
- [ ] 是否有被注释掉的代码
- [ ] 是否有修改痕迹（注释掉的历史值）
- [ ] 是否有拼音变量或方法名
- [ ] 是否有拼写错误的英文
- [ ] 是否有字符串状态码
- [ ] 路由是否直接调用数据库
- [ ] Service 是否直接写 SQL
- [ ] 是否有从未被调用的函数
