"""
服务路由器 - 根据负载均衡策略路由请求
"""
import random
from typing import List, Optional


class ServiceNode:
    """服务节点"""

    def __init__(self, node_id: str, host: str, port: int, weight: int = 1):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.weight = weight
        self.active = True

    def __str__(self):
        return f"{self.host}:{self.port}"


class ServiceRouter:
    """
    服务路由器

    支持多种负载均衡策略：
    - round_robin: 轮询
    - random: 随机
    - weighted: 加权
    - consistent_hash: 一致性哈希
    """

    def __init__(self, service_name: str, strategy: str = "random"):
        self.service_name = service_name
        self.strategy = strategy
        self.nodes: List[ServiceNode] = []
        self.current_index = 0

    def add_node(self, node: ServiceNode):
        """添加服务节点"""
        self.nodes.append(node)

    def remove_node(self, node_id: str):
        """移除服务节点"""
        self.nodes = [n for n in self.nodes if n.node_id != node_id]

    def route(self, key: Optional[str] = None) -> Optional[ServiceNode]:
        """
        路由请求

        Args:
            key: 路由键（如用户ID）

        Returns:
            目标服务节点
        """
        if not self.nodes:
            return None

        active_nodes = [n for n in self.nodes if n.active]
        if not active_nodes:
            return None

        if self.strategy == "round_robin":
            return self._round_robin(active_nodes)
        elif self.strategy == "random":
            return self._random(active_nodes)
        elif self.strategy == "weighted":
            return self._weighted(active_nodes)
        elif self.strategy == "consistent_hash":
            return self._consistent_hash(active_nodes, key)
        else:
            return active_nodes[0]

    def _round_robin(self, nodes: List[ServiceNode]) -> ServiceNode:
        node = nodes[self.current_index % len(nodes)]
        self.current_index += 1
        return node

    def _random(self, nodes: List[ServiceNode]) -> ServiceNode:
        return random.choice(nodes)

    def _weighted(self, nodes: List[ServiceNode]) -> ServiceNode:
        total_weight = sum(n.weight for n in nodes)
        r = random.randint(1, total_weight)
        for node in nodes:
            r -= node.weight
            if r <= 0:
                return node
        return nodes[-1]

    def _consistent_hash(self, nodes: List[ServiceNode], key: Optional[str]) -> ServiceNode:
        if not key:
            return nodes[0]
        hash_value = hash(key)
        index = hash_value % len(nodes)
        return nodes[index]
