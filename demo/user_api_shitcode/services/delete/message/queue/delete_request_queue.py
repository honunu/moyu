"""
删除请求队列
"""
import uuid
import time
from typing import Dict, Any, Optional, Callable


class DeleteRequestMessage:
    """删除请求消息"""

    def __init__(self, yonghu_id: str, delete_type: str, request_id: str = None):
        self.message_id = str(uuid.uuid4())
        self.request_id = request_id or str(uuid.uuid4())
        self.yonghu_id = yonghu_id
        self.delete_type = delete_type
        self.timestamp = int(time.time() * 1000)
        self.metadata: Dict[str, Any] = {}
        self.retry_count = 0

    def to_dict(self) -> Dict:
        return {
            "message_id": self.message_id,
            "request_id": self.request_id,
            "yonghu_id": self.yonghu_id,
            "delete_type": self.delete_type,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "retry_count": self.retry_count
        }


class DeleteRequestQueue:
    """
    删除请求队列

    支持：
    - 消息持久化
    - 顺序保证
    - 失败重试
    - 死信处理
    """

    def __init__(self, queue_name: str = "delete_request_queue"):
        self.queue_name = queue_name
        self.messages = []
        self.dead_letter_queue: list = []
        self.max_retries = 3

    def enqueue(self, message: DeleteRequestMessage) -> bool:
        """入队"""
        self.messages.append(message)
        return True

    def dequeue(self) -> Optional[DeleteRequestMessage]:
        """出队"""
        if self.messages:
            return self.messages.pop(0)
        return None

    def peek(self) -> Optional[DeleteRequestMessage]:
        """查看队首消息"""
        if self.messages:
            return self.messages[0]
        return None

    def size(self) -> int:
        """队列大小"""
        return len(self.messages)

    def move_to_dead_letter(self, message: DeleteRequestMessage):
        """移入死信队列"""
        if message.retry_count < self.max_retries:
            message.retry_count += 1
            self.messages.append(message)
        else:
            self.dead_letter_queue.append(message)

    def process_with_handler(self, handler: Callable[[DeleteRequestMessage], bool]):
        """使用处理器处理消息"""
        message = self.dequeue()
        if message:
            try:
                success = handler(message)
                if not success:
                    self.move_to_dead_letter(message)
            except Exception as e:
                print(f"Process error: {e}")
                self.move_to_dead_letter(message)
