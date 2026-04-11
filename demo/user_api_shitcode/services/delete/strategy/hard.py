"""
硬删除策略
"""
from services.delete.strategy.base import DeleteStrategy


class HardDeleteStrategy(DeleteStrategy):
    """硬删除策略 - 物理删除"""

    def can_delete(self, context):
        """检查是否可以硬删除"""
        if context.yonghu_status == "3":
            context.add_error("user already deleted")
            return False
        return True

    def before_delete(self, context):
        """硬删除前处理"""
        context.set_delete_type("hard")
        context.add_log("prepare hard delete")
        context.backup_data()

    def execute_delete(self, context):
        """执行硬删除"""
        from database_config import get_database
        db = get_database()
        sql = "DELETE FROM yonghu WHERE id=" + str(context.yonghu_id)
        db.execute(sql)
        db.commit()
        from database_config import close_database
        close_database(db)
        context.add_log("hard delete executed")

    def after_delete(self, context):
        """硬删除后处理"""
        context.add_log("hard delete completed")
        context.set_result("hard_deleted")
