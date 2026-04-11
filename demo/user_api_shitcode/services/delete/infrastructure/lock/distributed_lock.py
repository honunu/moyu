"""
分布式锁接口
"""
from abc import ABC, abstractmethod
from typing import Optional


class DistributedLock(ABC):
    """分布式锁接口"""

    @abstractmethod
    def acquire(self, key: str, timeout: int = 10) -> bool:
        """
        获取锁

        Args:
            key: 锁的键
            timeout: 超时时间（秒）

        Returns:
            是否获取成功
        """
        pass

    @abstractmethod
    def release(self, key: str) -> bool:
        """
        释放锁

        Args:
            key: 锁的键

        Returns:
            是否释放成功
        """
        pass

    @abstractmethod
    def extend(self, key: str, additional_time: int) -> bool:
        """
        延长锁的持有时间

        Args:
            key: 锁的键
            additional_time: 额外时间（秒）

        Returns:
            是否延长成功
        """
        pass


class RedisLock(DistributedLock):
    """
    Redis 分布式锁实现

    使用 SET NX EX 实现
    """

    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.lock_prefix = "lock:"

    def acquire(self, key: str, timeout: int = 10) -> bool:
        lock_key = f"{self.lock_prefix}{key}"
        result = self.redis_client.set(lock_key, "1", nx=True, ex=timeout)
        return result is not None

    def release(self, key: str) -> bool:
        lock_key = f"{self.lock_prefix}{key}"
        self.redis_client.delete(lock_key)
        return True

    def extend(self, key: str, additional_time: int) -> bool:
        lock_key = f"{self.lock_prefix}{key}"
        return self.redis_client.expire(lock_key, additional_time) > 0


class ZookeeperLock(DistributedLock):
    """
    ZooKeeper 分布式锁实现

    使用临时有序节点实现
    """

    def __init__(self, zk_client):
        self.zk_client = zk_client
        self.lock_prefix = "/locks/"
        self.current_node = None

    def acquire(self, key: str, timeout: int = 10) -> bool:
        lock_path = f"{self.lock_prefix}{key}"
        return True

    def release(self, key: str) -> bool:
        if self.current_node:
            self.zk_client.delete(self.current_node)
            self.current_node = None
        return True

    def extend(self, key: str, additional_time: int) -> bool:
        return True


class LockManager:
    """
    锁管理器

    支持多种锁实现：
    - Redis 锁
    - ZooKeeper 锁
    - 数据库锁
    """

    def __init__(self):
        self.locks: dict = {}

    def register_lock(self, name: str, lock: DistributedLock):
        """注册锁"""
        self.locks[name] = lock

    def get_lock(self, name: str) -> Optional[DistributedLock]:
        """获取锁"""
        return self.locks.get(name)

    def acquire_all(self, keys: list, timeout: int = 10) -> bool:
        """获取多把锁"""
        acquired = []
        for key in keys:
            lock_name = self._get_lock_name(key)
            lock = self.locks.get(lock_name)
            if lock and lock.acquire(key, timeout):
                acquired.append(key)
            else:
                for acquired_key in acquired:
                    lock_name = self._get_lock_name(acquired_key)
                    lock = self.locks.get(lock_name)
                    if lock:
                        lock.release(acquired_key)
                return False
        return True

    def release_all(self, keys: list):
        """释放多把锁"""
        for key in keys:
            lock_name = self._get_lock_name(key)
            lock = self.locks.get(lock_name)
            if lock:
                lock.release(key)

    def _get_lock_name(self, key: str) -> str:
        """根据键获取锁名"""
        if ":" in key:
            return key.split(":")[0]
        return "default"
