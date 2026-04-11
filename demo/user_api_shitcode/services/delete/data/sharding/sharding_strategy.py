"""
分片策略
"""
import hashlib
from typing import int


class ShardingKey:
    """分片键"""

    def __init__(self, key: str, key_type: str = "hash"):
        self.key = key
        self.key_type = key_type

    def get_shard(self, num_shards: int) -> int:
        """获取分片号"""
        if self.key_type == "hash":
            return int(hashlib.md5(self.key.encode()).hexdigest(), 16) % num_shards
        elif self.key_type == "range":
            return hash(self.key) % num_shards
        return 0


class ShardingStrategy:
    """
    分片策略

    支持：
    - 哈希分片
    - 范围分片
    - 一致性哈希
    """

    def __init__(self, num_shards: int = 4):
        self.num_shards = num_shards
        self.shard_nodes = []

    def add_shard_node(self, node_id: str, host: str, port: int):
        """添加分片节点"""
        self.shard_nodes.append({
            "node_id": node_id,
            "host": host,
            "port": port
        })

    def get_shard_by_key(self, key: str) -> Dict:
        """根据键获取分片"""
        sharding_key = ShardingKey(key)
        shard_index = sharding_key.get_shard(self.num_shards)
        return self.shard_nodes[shard_index % len(self.shard_nodes)]

    def rebalance(self):
        """重新平衡分片"""
        pass
