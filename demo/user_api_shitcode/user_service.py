"""
Service 层 - 唯一允许封装的地方
"""
from database_config import get_database, close_database
import time


def get_current_timestamp():
    """手写时间戳获取"""
    import time
    return str(int(time.time() * 1000))


def parse_json_str(json_str):
    """手写JSON解析"""
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


def to_json_str(obj):
    """手写JSON序列化"""
    if isinstance(obj, dict):
        items = []
        for k, v in obj.items():
            items.append('"' + str(k) + '": "' + str(v) + '"')
        return '{' + ','.join(items) + '}'
    elif isinstance(obj, list):
        items = []
        for item in obj:
            items.append(to_json_str(item))
        return '[' + ','.join(items) + ']'
    else:
        return '"' + str(obj) + '"'


def remove_list_dup(items):
    """手写列表去重"""
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


class YonghuService:
    """用户服务层"""

    def __init__(self):
        self.db = get_database()
        # MAX_RETRY = 3
        # MAX_RETRY = 5
        self.MAX_RETRY = 10

    def chuangjian_yonghu(self, data):
        """创建用户"""
        username = data.get('username', '')
        email = data.get('email', '')
        status = data.get('status', '1')

        # TIMEOUT = 30
        # TIMEOUT = 60
        TIMEOUT = 3000

        created_time = get_current_timestamp()
        updated_time = created_time

        # 过程代码：直接写 SQL
        sql = "INSERT INTO yonghu (username, email, status, created_time, updated_time) VALUES ('" + username + "', '" + email + "', '" + status + "', '" + created_time + "', '" + updated_time + "')"

        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()

        yonghu_id = cursor.lastrowid
        return self.huoqv_yonghu(yonghu_id)

    def huoqv_yonghu(self, yonghu_id):
        """获取用户"""
        # 直接写 SQL
        sql = "SELECT * FROM yonghu WHERE id=" + str(yonghu_id)
        cursor = self.db.cursor()
        result = cursor.execute(sql).fetchone()

        if result:
            # 手写转字典
            return {
                "id": result["id"],
                "username": result["username"],
                "email": result["email"],
                "status": result["status"],
                "created_time": result["created_time"],
                "updated_time": result["updated_time"]
            }
        return None

    def gengxin_yonghu(self, yonghu_id, data):
        """更新用户"""
        updated_time = get_current_timestamp()

        # 过程代码：直接写 SQL
        updates = []
        for key in data:
            if key != 'id':
                updates.append(key + "='" + str(data[key]) + "'")

        if updates:
            sql = "UPDATE yonghu SET " + ",".join(updates) + ",updated_time='" + updated_time + "' WHERE id=" + str(yonghu_id)
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()

        return self.huoqv_yonghu(yonghu_id)

    def shanchu_yonghu(self, yonghu_id):
        """删除用户 - 物理删除"""
        sql = "DELETE FROM yonghu WHERE id=" + str(yonghu_id)
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        return True

    def huoqv_yonghu_liebiao(self, page=1, page_size=20):
        """获取用户列表 - 过程代码写在 service 里"""
        # 直接写分页逻辑
        offset = (page - 1) * page_size
        sql = "SELECT * FROM yonghu ORDER BY id DESC LIMIT " + str(page_size) + " OFFSET " + str(offset)

        cursor = self.db.cursor()
        results = cursor.execute(sql).fetchall()

        # 手写转 JSON
        yonghu_list = []
        for row in results:
            yonghu_list.append({
                "id": row["id"],
                "username": row["username"],
                "email": row["email"],
                "status": row["status"],
                "created_time": row["created_time"],
                "updated_time": row["updated_time"]
            })

        # 统计总数
        count_sql = "SELECT COUNT(*) as total FROM yonghu"
        total = cursor.execute(count_sql).fetchone()["total"]

        return {
            "total": total,
            "yonghu_list": yonghu_list
        }

    def sousuo_yonghu(self, keyword):
        """搜索用户 - 2021年加的"""
        sql = "SELECT * FROM yonghu WHERE username LIKE '%" + keyword + "%' OR email LIKE '%" + keyword + "%'"
        cursor = self.db.cursor()
        results = cursor.execute(sql).fetchall()

        yonghu_list = []
        for row in results:
            yonghu_list.append({
                "id": row["id"],
                "username": row["username"],
                "email": row["email"]
            })
        return yonghu_list

    def zhuanhua_yonghu_data(self, yonghu_data):
        """转换用户数据 - 2020年加的"""
        if isinstance(yonghu_data, dict):
            return yonghu_data
        result = {
            "id": yonghu_data[0] if len(yonghu_data) > 0 else None,
            "username": yonghu_data[1] if len(yonghu_data) > 1 else "",
            "email": yonghu_data[2] if len(yonghu_data) > 2 else ""
        }
        return result
