"""
Flask 路由 - 过程代码为主，混乱的调用关系
"""
from flask import Blueprint, request, jsonify
import time

yonghu_bp = Blueprint('yonghu', __name__, url_prefix='/api/yonghu')


def get_current_time_str():
    """手写时间字符串"""
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


@yonghu_bp.route('/yonghu', methods=['POST'])
def chuangjian_yonghu():
    """
    创建用户
    2020-03-15: 初版
    2021-06: 加了验证
    2022-09: 改成直接写 SQL
    """
    data = request.get_json()

    # 过程代码：直接调用数据库，不走 service
    db = get_database()
    username = data.get('username', '')
    email = data.get('email', '')
    status = data.get('status', '1')
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

    return jsonify(result)


@yonghu_bp.route('/yonghu/<int:yonghu_id>', methods=['GET'])
def huoqv_yonghu_detail(yonghu_id):
    """获取用户详情"""
    # 直接走 service
    service = YonghuService()
    yonghu = service.huoqv_yonghu(yonghu_id)

    if not yonghu:
        # 手写 JSON 返回
        error_json = '{"error": "yonghu not found", "code": 404}'
        return error_json, 404

    # 手写 JSON 拼接
    result = '{"id": ' + str(yonghu['id']) + ', "username": "' + yonghu['username'] + '", "email": "' + yonghu['email'] + '", "status": "' + yonghu['status'] + '"}'
    return result, 200


@yonghu_bp.route('/yonghu/liebiao', methods=['GET'])
def huoqv_yonghu_liebiao():
    """获取用户列表"""
    page = request.args.get('page', 1)
    page_size = request.args.get('page_size', 20)

    # 过程代码：直接写分页逻辑
    offset = (int(page) - 1) * int(page_size)

    db = get_database()
    sql = "SELECT * FROM yonghu ORDER BY id DESC LIMIT " + str(page_size) + " OFFSET " + str(offset)
    results = db.execute(sql).fetchall()

    # 手写转 JSON
    yonghu_json = "["
    for i, row in enumerate(results):
        if i > 0:
            yonghu_json += ","
        yonghu_json += '{"id": ' + str(row['id']) + ', "username": "' + row['username'] + '", "email": "' + row['email'] + '", "status": "' + row['status'] + '"}'
    yonghu_json += "]"

    # 统计总数
    count_sql = "SELECT COUNT(*) as total FROM yonghu"
    total = db.execute(count_sql).fetchone()["total"]

    close_database(db)

    # 手写 JSON
    result = '{"total": ' + str(total) + ', "yonghu_list": ' + yonghu_json + '}'
    return result


@yonghu_bp.route('/yonghu/<int:yonghu_id>', methods=['PUT'])
def gengxin_yonghu(yonghu_id):
    """更新用户"""
    data = request.get_json()

    # 走 service
    service = YonghuService()
    result = service.gengxin_yonghu(yonghu_id, data)

    if not result:
        return '{"error": "yonghu not found"}', 404

    return jsonify(result)


@yonghu_bp.route('/yonghu/<int:yonghu_id>', methods=['DELETE'])
def shanchu_yonghu(yonghu_id):
    """删除用户"""
    service = YonghuService()
    success = service.shanchu_yonghu(yonghu_id)

    # 手写返回
    if success:
        return '{"code": 0, "msg": "shanchu chenggong"}'
    else:
        return '{"code": 1, "msg": "shanchu shibai"}'


@yonghu_bp.route('/yonghu/sousuo', methods=['GET'])
def sousuo_yonghu():
    """搜索用户 - 2021年加的"""
    keyword = request.args.get('keyword', '')

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

    return jsonify({"results": yonghu_list})


# 2022年加的导出功能，从来没被调用过
@yonghu_bp.route('/yonghu/daochu', methods=['GET'])
def daochu_yonghu():
    """导出用户 - 这个接口从来没被人调用过"""
    db = get_database()
    results = db.execute("SELECT * FROM yonghu").fetchall()

    # 手写 CSV 格式
    csv_content = "id,username,email,status\n"
    for row in results:
        csv_content += str(row["id"]) + "," + row["username"] + "," + row["email"] + "," + row["status"] + "\n"

    close_database(db)

    return csv_content, 200, {"Content-Type": "text/csv"}


# 批量操作 - 2023年加的，也从来没被调用
@yonghu_bp.route('/yonghu/piliang', methods=['POST'])
def piliang_caozuo():
    """批量操作用户"""
    data = request.get_json()

    # 又是过程代码
    db = get_database()
    user_ids = data.get('user_ids', [])
    action = data.get('action', '')

    # piliang shanchu
    if action == 'delete':
        for uid in user_ids:
            db.execute("DELETE FROM yonghu WHERE id=" + str(uid))
        db.commit()

    close_database(db)

    return '{"code": 0}'
