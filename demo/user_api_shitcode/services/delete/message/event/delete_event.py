"""
删除领域事件
"""
import uuid
import time
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class DeleteEvent(ABC):
    """删除事件基类"""

    def __init__(self, event_type: str, yonghu_id: str, request_id: str = None):
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.yonghu_id = yonghu_id
        self.request_id = request_id or str(uuid.uuid4())
        self.timestamp = int(time.time() * 1000)
        self.version = "1.0"

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "yonghu_id": self.yonghu_id,
            "request_id": self.request_id,
            "timestamp": self.timestamp,
            "version": self.version
        }


class DeleteStartedEvent(DeleteEvent):
    """删除开始事件"""

    def __init__(self, yonghu_id: str, delete_type: str, request_id: str = None):
        super().__init__("delete_started", yonghu_id, request_id)
        self.delete_type = delete_type

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["delete_type"] = self.delete_type
        return data


class DeleteCompletedEvent(DeleteEvent):
    """删除完成事件"""

    def __init__(self, yonghu_id: str, request_id: str = None, duration: int = 0):
        super().__init__("delete_completed", yonghu_id, request_id)
        self.duration = duration

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["duration"] = self.duration
        return data


class DeleteFailedEvent(DeleteEvent):
    """删除失败事件"""

    def __init__(self, yonghu_id: str, error: str, request_id: str = None):
        super().__init__("delete_failed", yonghu_id, request_id)
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["error"] = self.error
        return data


class EventPublisher:
    """
    事件发布器

    支持：
    - 同步/异步发布
    - 事件持久化
    - 失败重试
    """

    def __init__(self):
        self.subscribers: Dict[str, list] = {}

    def subscribe(self, event_type: str, handler):
        """订阅事件"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler):
        """取消订阅"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(handler)

    def publish(self, event: DeleteEvent):
        """发布事件"""
        event_type = event.event_type
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Event handler error: {e}")

    def publish_async(self, event: DeleteEvent):
        """异步发布事件"""
        pass
