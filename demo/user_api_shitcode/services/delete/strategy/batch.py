"""
批量删除策略
"""
from services.delete.strategy.base import DeleteStrategy


class BatchDeleteStrategy(DeleteStrategy):
    """批量删除策略"""

    def __init__(self):
        self.deleted_count = 0

    def can_delete(self, context):
        """检查是否可以批量删除"""
        if not context.yonghu_ids or len(context.yonghu_ids) == 0:
            context.add_error("no users to delete")
            return False
        return True

    def before_delete(self, context):
        """批量删除前处理"""
        context.set_delete_type("batch")
        context.add_log("prepare batch delete")
        self.deleted_count = 0

    def execute_delete(self, context):
        """执行批量删除"""
        from database_config import get_database
        db = get_database()
        for uid in context.yonghu_ids:
            sql = "DELETE FROM yonghu WHERE id=" + str(uid)
            db.execute(sql)
            self.deleted_count += 1
        db.commit()
        from database_config import close_database
        close_database(db)
        context.add_log("batch delete executed")

    def after_delete(self, context):
        """批量删除后处理"""
        context.set_result("batch_deleted", {"count": self.deleted_count})
        context.add_log("batch delete completed")
