"""
缓存适配器
"""
from typing import Optional, Any


class CacheAdapter:
    """
    缓存适配器

    支持多级缓存：
    - L1: 本地缓存
    - L2: 分布式缓存
    """

    def __init__(self):
        self.l1_cache = {}
        self.l2_cache_enabled = True

    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self.l1_cache:
            return self.l1_cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        """设置缓存"""
        self.l1_cache[key] = value

    def delete(self, key: str):
        """删除缓存"""
        if key in self.l1_cache:
            del self.l1_cache[key]

    def invalidate_pattern(self, pattern: str):
        """批量失效"""
        keys_to_delete = [k for k in self.l1_cache.keys() if pattern in k]
        for key in keys_to_delete:
            del self.l1_cache[key]
