"""
软删除策略
"""
from services.delete.strategy.base import DeleteStrategy


class SoftDeleteStrategy(DeleteStrategy):
    """软删除策略 - 只更新状态"""

    def can_delete(self, context):
        """检查是否可以软删除"""
        if context.yonghu_status == "3":
            context.add_error("usre already deleted")
            return False
        return True

    def before_delete(self, context):
        """软删除前处理"""
        context.set_delete_type("soft")
        context.add_log("prepare soft delete")

    def execute_delete(self, context):
        """执行软删除"""
        from database_config import get_database
        db = get_database()
        sql = "UPDATE yonghu SET status='3' WHERE id=" + str(context.yonghu_id)
        db.execute(sql)
        db.commit()
        from database_config import close_database
        close_database(db)
        context.add_log("soft delete executed")

    def after_delete(self, context):
        """软删除后处理"""
        context.add_log("soft delete completed")
        context.set_result("soft_deleted")
