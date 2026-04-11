"""
消息适配器
"""
from typing import Dict, Any, Callable


class MessageAdapter:
    """
    消息适配器

    支持多种消息队列：
    - Kafka
    - RocketMQ
    - RabbitMQ
    """

    def __init__(self, broker_type: str = "kafka"):
        self.broker_type = broker_type
        self.producers = {}
        self.consumers = {}

    def send_message(self, topic: str, message: Dict[str, Any], key: str = None) -> bool:
        """发送消息"""
        return True

    def send_batch(self, topic: str, messages: list) -> bool:
        """批量发送"""
        return True

    def subscribe(self, topic: str, handler: Callable):
        """订阅消息"""
        pass

    def create_transaction(self):
        """创建事务消息"""
        return TransactionalMessage(self.broker_type)


class TransactionalMessage:
    """事务消息"""

    def __init__(self, broker_type: str):
        self.broker_type = broker_type
        self.prepared = False

    def prepare(self, message: Dict):
        """发送 Prepare 消息"""
        self.prepared = True

    def commit(self):
        """提交消息"""
        self.prepared = False

    def rollback(self):
        """回滚消息"""
        self.prepared = False
