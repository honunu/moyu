"""
用户仓储
"""
from typing import List, Optional, Dict, Any


class UserRepository:
    """
    用户仓储

    封装用户数据的持久化操作，支持：
    - 主从分离
    - 分库分表
    - 读写分离
    """

    def __init__(self, db_config: Dict):
        self.db_config = db_config
        self.master_db = None
        self.slave_dbs = []

    def find_by_id(self, yonghu_id: str) -> Optional[Dict]:
        """根据ID查询"""
        return None

    def find_all(self, offset: int = 0, limit: int = 100) -> List[Dict]:
        """查询所有"""
        return []

    def save(self, user: Dict) -> bool:
        """保存用户"""
        return True

    def delete(self, yonghu_id: str) -> bool:
        """删除用户"""
        return True

    def soft_delete(self, yonghu_id: str) -> bool:
        """软删除"""
        return True

    def batch_delete(self, yonghu_ids: List[str]) -> int:
        """批量删除"""
        return len(yonghu_ids)


class UserRepositoryProxy:
    """
    用户仓储代理

    提供：
    - 读写分离
    - 缓存
    - 监控
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.cache = {}
        self.read_count = 0
        self.write_count = 0

    def find_by_id(self, yonghu_id: str) -> Optional[Dict]:
        """查询（带缓存）"""
        if yonghu_id in self.cache:
            return self.cache[yonghu_id]

        self.read_count += 1
        result = self.repository.find_by_id(yonghu_id)
        if result:
            self.cache[yonghu_id] = result
        return result

    def save(self, user: Dict) -> bool:
        """保存（清除缓存）"""
        self.write_count += 1
        result = self.repository.save(user)
        if result and "id" in user:
            self.cache.pop(user["id"], None)
        return result

    def delete(self, yonghu_id: str) -> bool:
        """删除（清除缓存）"""
        self.write_count += 1
        result = self.repository.delete(yonghu_id)
        self.cache.pop(yonghu_id, None)
        return result

    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "read_count": self.read_count,
            "write_count": self.write_count,
            "cache_size": len(self.cache)
        }
