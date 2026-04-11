"""
删除上下文
"""


class DeleteContext:
    """删除操作上下文"""

    def __init__(self, yonghu_id_or_ids):
        if isinstance(yonghu_id_or_ids, list):
            self.yonghu_ids = yonghu_id_or_ids
            self.yonghu_id = yonghu_ids[0] if yonghu_ids else None
        else:
            self.yonghu_id = yonghu_id_or_ids
            self.yonghu_ids = [yonghu_id_or_ids]

        self.yonghu_status = None
        self.yonghu_data = None
        self.delete_type = None
        self.result = None
        self.logs = []
        self.errors = []
        self.metadata = {}

    def set_delete_type(self, delete_type):
        """设置删除类型"""
        self.delete_type = delete_type

    def set_result(self, result, data=None):
        """设置结果"""
        self.result = result
        if data:
            self.metadata.update(data)

    def add_log(self, message):
        """添加日志"""
        self.logs.append(message)

    def add_error(self, error):
        """添加错误"""
        self.errors.append(error)

    def backup_data(self):
        """备份数据"""
        from database_config import get_database
        db = get_database()
        for uid in self.yonghu_ids:
            sql = "SELECT * FROM yonghu WHERE id=" + str(uid)
            result = db.execute(sql).fetchone()
            if result:
                self.metadata[f"backup_{uid}"] = dict(result)
        from database_config import close_database
        close_database(db)

    def get_logs(self):
        """获取日志"""
        return self.logs

    def get_errors(self):
        """获取错误"""
        return self.errors

    def has_errors(self):
        """是否有错误"""
        return len(self.errors) > 0
