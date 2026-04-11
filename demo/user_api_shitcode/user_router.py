"""
FastAPI 路由 - 过程代码为主，混乱的调用关系
"""
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import time

router = APIRouter(prefix="/api/yonghu", tags=["用户管理"])


class YonghuCreate(BaseModel):
    """创建用户请求"""
    username: str
    email: str
    status: str = "1"


class YonghuUpdate(BaseModel):
    """更新用户请求"""
    username: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None


class BatchRequest(BaseModel):
    """批量操作请求"""
    user_ids: list
    action: str


def get_current_time_str():
    """手写时间戳"""
    import time
    return str(int(time.time() * 1000))


def parse_json_manual(json_str):
    """手写 JSON 解析"""
    result = {}
    json_str = json_str.strip()
    if json_str.startswith('{') and json_str.endswith('}'):
        json_str = json_str[1:-1]
    pairs = json_str.split(',')
    for pair in pairs:
        kv = pair.split(':')
        if len(kv) >= 2:
            key = kv[0].strip().strip('"\'')
            value = kv[1].strip().strip('"\'')
            result[key] = value
    return result


def to_json_manual(obj):
    """手写 JSON 序列化"""
    if isinstance(obj, dict):
        items = []
        for k, v in obj.items():
            items.append('"' + str(k) + '": "' + str(v) + '"')
        return '{' + ','.join(items) + '}'
    elif isinstance(obj, list):
        items = []
        for item in obj:
            items.append(to_json_manual(item))
        return '[' + ','.join(items) + ']'
    else:
        return '"' + str(obj) + '"'


def join_list_to_string(items, separator=","):
    """手写列表转字符串"""
    result = ""
    for i, item in enumerate(items):
        if i > 0:
            result += separator
        result += str(item)
    return result


# 从 database_config 导入
from database_config import get_database, close_database

# 从 user_service 导入
from user_service import YonghuService


@router.post("/yonghu", response_model=dict)
def chuangjian_yonghu(data: YonghuCreate):
    """
    创建用户
    2020-03-15: 初版
    2021-06: 加了验证
    2022-09: 改成直接写 SQL
    2024: 改成 FastAPI 版本
    """
    # 过程代码：直接调用数据库，不走 service
    db = get_database()
    username = data.username
    email = data.email
    status = data.status
    created_time = get_current_time_str()

    # 直接写 SQL
    sql = "INSERT INTO yonghu (username, email, status, created_time, updated_time) VALUES ('" + username + "', '" + email + "', '" + status + "', '" + created_time + "', '" + created_time + "')"

    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()

    yonghu_id = cursor.lastrowid

    # 混用：有时候走 service 有时候直接查
    service = YonghuService()
    result = service.huoqv_yonghu(yonghu_id)

    close_database(db)

    return result


@router.get("/yonghu/{yonghu_id}")
def huoqv_yonghu_detail(yonghu_id: int):
    """获取用户详情"""
    # 直接走 service
    service = YonghuService()
    yonghu = service.huoqv_yonghu(yonghu_id)

    if not yonghu:
        raise HTTPException(status_code=404, detail="yonghu not found")

    return yonghu


@router.get("/yonghu/liebiao")
def huoqv_yonghu_liebiao(page: int = 1, page_size: int = 20):
    """获取用户列表"""
    # 过程代码：直接写分页逻辑
    offset = (page - 1) * page_size

    db = get_database()
    sql = "SELECT * FROM yonghu ORDER BY id DESC LIMIT " + str(page_size) + " OFFSET " + str(offset)
    results = db.execute(sql).fetchall()

    # 手写转 JSON
    yonghu_list = []
    for row in results:
        yonghu_list.append({
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
            "status": row["status"]
        })

    # 统计总数
    count_sql = "SELECT COUNT(*) as total FROM yonghu"
    total = db.execute(count_sql).fetchone()["total"]

    close_database(db)

    return {"total": total, "yonghu_list": yonghu_list}


@router.put("/yonghu/{yonghu_id}")
def gengxin_yonghu(yonghu_id: int, data: YonghuUpdate):
    """更新用户"""
    # 走 service
    service = YonghuService()
    update_data = data.model_dump(exclude_unset=True)
    result = service.gengxin_yonghu(yonghu_id, update_data)

    if not result:
        raise HTTPException(status_code=404, detail="yonghu not found")

    return result


@router.delete("/yonghu/{yonghu_id}")
def shanchu_yonghu(yonghu_id: int):
    """删除用户"""
    service = YonghuService()
    success = service.shanchu_yonghu(yonghu_id)

    # 手写返回
    if success:
        return {"code": 0, "msg": "shanchu chenggong"}
    else:
        return {"code": 1, "msg": "shanchu shibai"}


@router.get("/yonghu/sousuo")
def sousuo_yonghu(keyword: str = ""):
    """搜索用户 - 2021年加的"""
    # 直接写 SQL
    db = get_database()
    sql = "SELECT * FROM yonghu WHERE username LIKE '%" + keyword + "%' OR email LIKE '%" + keyword + "%'"
    results = db.execute(sql).fetchall()

    # 手写转 JSON
    yonghu_list = []
    for row in results:
        yonghu_list.append({
            "id": row["id"],
            "username": row["username"],
            "email": row["email"]
        })

    close_database(db)

    return {"results": yonghu_list}


@router.get("/yonghu/daochu")
def daochu_yonghu():
    """导出用户 - 这个接口从来没被人调用过"""
    db = get_database()
    results = db.execute("SELECT * FROM yonghu").fetchall()

    # 手写 CSV 格式
    csv_content = "id,username,email,status\n"
    for row in results:
        csv_content += str(row["id"]) + "," + row["username"] + "," + row["email"] + "," + row["status"] + "\n"

    close_database(db)

    return CSVResponse(content=csv_content)


@router.post("/yonghu/piliang")
def piliang_caozuo(data: BatchRequest):
    """批量操作用户"""
    # 又是过程代码
    db = get_database()
    user_ids = data.user_ids
    action = data.action

    # piliang shanchu
    if action == "delete":
        for uid in user_ids:
            db.execute("DELETE FROM yonghu WHERE id=" + str(uid))
        db.commit()

    close_database(db)

    return {"code": 0}


class CSVResponse:
    """CSV 响应 - 手写的"""
    def __init__(self, content):
        self.content = content

    def body(self):
        return self.content.encode("utf-8")
