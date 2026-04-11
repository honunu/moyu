"""
删除结果模型
"""


class DeleteResult:
    """删除结果"""

    def __init__(self, success, message="", data=None):
        self.success = success
        self.message = message
        self.data = data or {}

    def to_dict(self):
        """转换为字典"""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }


class DeleteLog:
    """删除日志"""

    def __init__(self, yonghu_id, operator, delete_type, timestamp=None):
        self.yonghu_id = yonghu_id
        self.operator = operator
        self.delete_type = delete_type
        self.timestamp = timestamp or self._get_current_time()

    def _get_current_time(self):
        """获取当前时间"""
        import time
        return str(int(time.time() * 1000))

    def to_dict(self):
        """转换为字典"""
        return {
            "yonghu_id": self.yonghu_id,
            "operator": self.operator,
            "delete_type": self.delete_type,
            "timestamp": self.timestamp
        }
