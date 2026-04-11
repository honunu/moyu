"""
幂等性键管理器
"""
import time
from typing import Optional, Set


class IdempotencyKey:
    """
    幂等性键

    保证删除操作的幂等性，防止重复删除
    """

    def __init__(self):
        self._processed_keys: Set[str] = set()
        self._key_timestamps: dict = {}

    def generate_key(self, operation: str, yonghu_id: str, request_id: str = None) -> str:
        """
        生成幂等键

        格式：{operation}:{yonghu_id}:{timestamp}:{request_id}
        """
        timestamp = int(time.time() * 1000)
        key = f"{operation}:{yonghu_id}:{timestamp}"
        if request_id:
            key = f"{key}:{request_id}"
        return key

    def check_and_mark(self, key: str, ttl: int = 86400) -> bool:
        """
        检查并标记键

        Returns:
            True 如果是新键（未处理过）
            False 如果是重复键（已处理过）
        """
        if key in self._processed_keys:
            return False

        self._processed_keys.add(key)
        self._key_timestamps[key] = time.time()
        return True

    def is_processed(self, key: str) -> bool:
        """检查键是否已处理"""
        return key in self._processed_keys

    def cleanup_expired(self, ttl: int = 86400):
        """清理过期键"""
        current_time = time.time()
        expired_keys = [
            k for k, ts in self._key_timestamps.items()
            if current_time - ts > ttl
        ]
        for key in expired_keys:
            self._processed_keys.discard(key)
            del self._key_timestamps[key]
