"""
删除管道
"""
from services.delete.validator.validator_chain import DeleteValidatorChain
from services.delete.observer.observer_manager import DeleteObserverManager


class DeletePipeline:
    """删除操作管道"""

    def __init__(self):
        self.validator_chain = DeleteValidatorChain()
        self.observer_manager = DeleteObserverManager()
        self.pre_processors = []
        self.post_processors = []

    def add_preprocessor(self, processor):
        """添加预处理器"""
        self.pre_processors.append(processor)

    def add_postprocessor(self, processor):
        """添加后处理器"""
        self.post_processors.append(processor)

    def execute(self, context, strategy):
        """执行删除管道"""
        self.observer_manager.notify_before_delete(context)

        if not self.validator_chain.validate(context):
            return False

        for processor in self.pre_processors:
            processor.process(context)

        if not strategy.can_delete(context):
            self.observer_manager.notify_delete_failed(context)
            return False

        strategy.before_delete(context)
        strategy.execute_delete(context)
        strategy.after_delete(context)

        for processor in self.post_processors:
            processor.process(context)

        self.observer_manager.notify_after_delete(context)

        return True
