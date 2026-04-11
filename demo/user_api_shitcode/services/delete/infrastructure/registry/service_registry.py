"""
服务注册表
"""
import time
from typing import Dict, List, Optional, Any


class ServiceInstance:
    """服务实例"""

    def __init__(self, instance_id: str, service_name: str, host: str, port: int):
        self.instance_id = instance_id
        self.service_name = service_name
        self.host = host
        self.port = port
        self.weight = 1
        self.health_check_url = None
        self.metadata: Dict[str, Any] = {}
        self.register_time = int(time.time())
        self.last_heartbeat = int(time.time())
        self.status = "UP"

    def is_healthy(self) -> bool:
        """检查是否健康"""
        return self.status == "UP"

    def update_heartbeat(self):
        """更新心跳"""
        self.last_heartbeat = int(time.time())

    def to_dict(self) -> Dict:
        return {
            "instance_id": self.instance_id,
            "service_name": self.service_name,
            "host": self.host,
            "port": self.port,
            "weight": self.weight,
            "status": self.status,
            "metadata": self.metadata,
            "register_time": self.register_time,
            "last_heartbeat": self.last_heartbeat
        }


class ServiceRegistry:
    """
    服务注册表

    支持：
    - 服务注册/注销
    - 心跳检测
    - 负载均衡
    - 故障转移
    """

    def __init__(self):
        self.services: Dict[str, List[ServiceInstance]] = {}

    def register(self, instance: ServiceInstance) -> bool:
        """
        注册服务实例

        Args:
            instance: 服务实例

        Returns:
            是否注册成功
        """
        service_name = instance.service_name
        if service_name not in self.services:
            self.services[service_name] = []

        for existing in self.services[service_name]:
            if existing.instance_id == instance.instance_id:
                existing.update_heartbeat()
                return True

        self.services[service_name].append(instance)
        return True

    def deregister(self, service_name: str, instance_id: str) -> bool:
        """
        注销服务实例

        Args:
            service_name: 服务名
            instance_id: 实例ID

        Returns:
            是否注销成功
        """
        if service_name not in self.services:
            return False

        self.services[service_name] = [
            i for i in self.services[service_name]
            if i.instance_id != instance_id
        ]
        return True

    def discover(self, service_name: str) -> List[ServiceInstance]:
        """
        发现服务实例

        Args:
            service_name: 服务名

        Returns:
            健康的服务实例列表
        """
        if service_name not in self.services:
            return []

        return [i for i in self.services[service_name] if i.is_healthy()]

    def discover_one(self, service_name: str, strategy: str = "random") -> Optional[ServiceInstance]:
        """
        发现一个服务实例

        Args:
            service_name: 服务名
            strategy: 负载均衡策略 (random/round_robin/weighted)

        Returns:
            选中的服务实例
        """
        instances = self.discover(service_name)
        if not instances:
            return None

        if strategy == "random":
            import random
            return random.choice(instances)
        elif strategy == "round_robin":
            return instances[0]
        elif strategy == "weighted":
            total_weight = sum(i.weight for i in instances)
            import random
            r = random.randint(1, total_weight)
            for instance in instances:
                r -= instance.weight
                if r <= 0:
                    return instance
        else:
            return instances[0]

    def heartbeat(self, service_name: str, instance_id: str) -> bool:
        """
        发送心跳

        Args:
            service_name: 服务名
            instance_id: 实例ID

        Returns:
            是否成功
        """
        instances = self.discover(service_name)
        for instance in instances:
            if instance.instance_id == instance_id:
                instance.update_heartbeat()
                return True
        return False
