"""
删除策略工厂
"""
from services.delete.strategy.soft import SoftDeleteStrategy
from services.delete.strategy.hard import HardDeleteStrategy
from services.delete.strategy.batch import BatchDeleteStrategy


class DeleteStrategyFactory:
    """删除策略工厂"""

    def __init__(self):
        self.registry = {
            "soft": SoftDeleteStrategy,
            "hard": HardDeleteStrategy,
            "batch": BatchDeleteStrategy,
        }

    def create_strategy(self, context):
        """根据上下文创建策略"""
        if len(context.yonghu_ids) > 1:
            return BatchDeleteStrategy()

        yonghu_id = context.yonghu_id

        from database_config import get_database
        db = get_database()
        sql = "SELECT status FROM yonghu WHERE id=" + str(yonghu_id)
        result = db.execute(sql).fetchone()
        from database_config import close_database
        close_database(db)

        if result:
            context.yonghu_status = result["status"]

        return SoftDeleteStrategy()

    def register_strategy(self, name, strategy_class):
        """注册新策略"""
        self.registry[name] = strategy_class

    def get_strategy_names(self):
        """获取所有策略名称"""
        return list(self.registry.keys())
