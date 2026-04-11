"""
删除策略基类
"""
from abc import ABC, abstractmethod


class DeleteStrategy(ABC):
    """删除策略基类"""

    @abstractmethod
    def can_delete(self, context):
        """检查是否可以删除"""
        pass

    @abstractmethod
    def before_delete(self, context):
        """删除前处理"""
        pass

    @abstractmethod
    def execute_delete(self, context):
        """执行删除"""
        pass

    @abstractmethod
    def after_delete(self, context):
        """删除后处理"""
        pass
