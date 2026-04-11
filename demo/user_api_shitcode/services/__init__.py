"""
删除服务入口
"""
from services.delete.context import DeleteContext
from services.delete.factory import DeleteStrategyFactory
from services.delete.pipeline import DeletePipeline


class YonghuDeleteService:
    """用户删除服务 - 过度工程化版本"""

    def __init__(self):
        self.factory = DeleteStrategyFactory()
        self.pipeline = DeletePipeline()

    def shanchu_yonghu(self, yonghu_id):
        """删除用户"""
        context = DeleteContext(yonghu_id)
        strategy = self.factory.create_strategy(context)
        return self.pipeline.execute(context, strategy)
