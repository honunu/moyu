"""
分布式观察者管理器
"""
from typing import List, Dict, Any, Callable
from abc import ABC, abstractmethod


class DeleteObserver(ABC):
    """删除观察者接口"""

    @abstractmethod
    def on_delete_started(self, event: Dict[str, Any]):
        """删除开始通知"""
        pass

    @abstractmethod
    def on_delete_completed(self, event: Dict[str, Any]):
        """删除完成通知"""
        pass

    @abstractmethod
    def on_delete_failed(self, event: Dict[str, Any]):
        """删除失败通知"""
        pass


class EmailObserver(DeleteObserver):
    """邮件观察者"""

    def __init__(self, smtp_config: Dict):
        self.smtp_config = smtp_config

    def on_delete_started(self, event: Dict[str, Any]):
        """发送删除开始邮件"""
        pass

    def on_delete_completed(self, event: Dict[str, Any]):
        """发送删除完成邮件"""
        pass

    def on_delete_failed(self, event: Dict[str, Any]):
        """发送删除失败邮件"""
        pass


class SmsObserver(DeleteObserver):
    """短信观察者"""

    def __init__(self, sms_config: Dict):
        self.sms_config = sms_config

    def on_delete_started(self, event: Dict[str, Any]):
        """发送删除开始短信"""
        pass

    def on_delete_completed(self, event: Dict[str, Any]):
        """发送删除完成短信"""
        pass

    def on_delete_failed(self, event: Dict[str, Any]):
        """发送删除失败短信"""
        pass


class WebhookObserver(DeleteObserver):
    """Webhook 观察者"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def on_delete_started(self, event: Dict[str, Any]):
        """发送 Webhook 通知"""
        pass

    def on_delete_completed(self, event: Dict[str, Any]):
        """发送 Webhook 通知"""
        pass

    def on_delete_failed(self, event: Dict[str, Any]):
        """发送 Webhook 通知"""
        pass


class DistributedObserverManager:
    """
    分布式观察者管理器

    支持：
    - 多个观察者订阅
    - 异步通知
    - 消息队列解耦
    - 失败重试
    """

    def __init__(self):
        self.observers: List[DeleteObserver] = []
        self.event_queue: List[Dict] = []
        self.retry_config = {"max_retries": 3, "retry_interval": 5}

    def register_observer(self, observer: DeleteObserver):
        """注册观察者"""
        self.observers.append(observer)

    def unregister_observer(self, observer: DeleteObserver):
        """取消注册"""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_delete_started(self, event: Dict[str, Any]):
        """通知删除开始"""
        for observer in self.observers:
            try:
                observer.on_delete_started(event)
            except Exception as e:
                print(f"Notify error: {e}")

    def notify_delete_completed(self, event: Dict[str, Any]):
        """通知删除完成"""
        for observer in self.observers:
            try:
                observer.on_delete_completed(event)
            except Exception as e:
                print(f"Notify error: {e}")

    def notify_delete_failed(self, event: Dict[str, Any]):
        """通知删除失败"""
        for observer in self.observers:
            try:
                observer.on_delete_failed(event)
            except Exception as e:
                print(f"Notify error: {e}")

    def add_async_event(self, event_type: str, event: Dict[str, Any]):
        """添加异步事件到队列"""
        self.event_queue.append({
            "type": event_type,
            "data": event,
            "retries": 0
        })

    def process_event_queue(self):
        """处理事件队列"""
        while self.event_queue:
            event = self.event_queue.pop(0)
            try:
                if event["type"] == "started":
                    self.notify_delete_started(event["data"])
                elif event["type"] == "completed":
                    self.notify_delete_completed(event["data"])
                elif event["type"] == "failed":
                    self.notify_delete_failed(event["data"])
            except Exception as e:
                if event["retries"] < self.retry_config["max_retries"]:
                    event["retries"] += 1
                    self.event_queue.append(event)
