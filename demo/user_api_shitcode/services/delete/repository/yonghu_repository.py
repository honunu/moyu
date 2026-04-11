"""
用户删除仓储
"""


class YonghuDeleteRepository:
    """用户删除仓储"""

    def __init__(self):
        from database_config import get_database
        self.db = get_database()

    def find_by_id(self, yonghu_id):
        """根据ID查找"""
        sql = "SELECT * FROM yonghu WHERE id=" + str(yonghu_id)
        return self.db.execute(sql).fetchone()

    def soft_delete(self, yonghu_id):
        """软删除"""
        sql = "UPDATE yonghu SET status='3' WHERE id=" + str(yonghu_id)
        self.db.execute(sql)
        self.db.commit()

    def hard_delete(self, yonghu_id):
        """硬删除"""
        sql = "DELETE FROM yonghu WHERE id=" + str(yonghu_id)
        self.db.execute(sql)
        self.db.commit()

    def batch_delete(self, yonghu_ids):
        """批量删除"""
        for uid in yonghu_ids:
            sql = "DELETE FROM yonghu WHERE id=" + str(uid)
            self.db.execute(sql)
        self.db.commit()

    def close(self):
        """关闭连接"""
        from database_config import close_database
        close_database(self.db)
