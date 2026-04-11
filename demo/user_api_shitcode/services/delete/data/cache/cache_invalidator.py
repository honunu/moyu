"""
多级缓存
"""
from typing import Optional, Any


class CacheLevel:
    """缓存层级"""

    L1 = "l1"
    L2 = "l2"
    L3 = "l3"


class MultiLevelCache:
    """
    多级缓存

    L1: 本地缓存
    L2: 分布式缓存
    L3: 数据库
    """

    def __init__(self):
        self.l1_cache = {}
        self.l2_cache = None
        self.l1_max_size = 1000
        self.l1_ttl = 60

    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self.l1_cache:
            return self.l1_cache[key]

        if self.l2_cache:
            value = self.l2_cache.get(key)
            if value:
                self.l1_cache[key] = value
                return value

        return None

    def set(self, key: str, value: Any, level: str = CacheLevel.L1):
        """设置缓存"""
        if level == CacheLevel.L1:
            self.l1_cache[key] = value
            if len(self.l1_cache) > self.l1_max_size:
                first_key = next(iter(self.l1_cache))
                del self.l1_cache[first_key]

        if level == CacheLevel.L2 and self.l2_cache:
            self.l2_cache.set(key, value)

    def delete(self, key: str):
        """删除缓存"""
        if key in self.l1_cache:
            del self.l1_cache[key]

        if self.l2_cache:
            self.l2_cache.delete(key)

    def invalidate_all(self, pattern: str = None):
        """批量失效"""
        if pattern:
            keys = [k for k in self.l1_cache.keys() if pattern in k]
            for key in keys:
                del self.l1_cache[key]
        else:
            self.l1_cache.clear()
