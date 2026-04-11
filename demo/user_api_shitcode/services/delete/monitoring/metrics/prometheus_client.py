"""
Prometheus 指标客户端
"""
import time
from typing import Dict, List, Any
from collections import defaultdict


class Counter:
    """计数器"""

    def __init__(self, name: str, description: str = "", labels: List[str] = None):
        self.name = name
        self.description = description
        self.labels = labels or []
        self._values: Dict[tuple, float] = defaultdict(float)

    def inc(self, value: float = 1, **label_values):
        """增加计数"""
        key = self._get_label_key(label_values)
        self._values[key] += value

    def _get_label_key(self, label_values: Dict) -> tuple:
        return tuple(label_values.get(l, "") for l in self.labels)

    def get(self, **label_values) -> float:
        """获取当前值"""
        key = self._get_label_key(label_values)
        return self._values.get(key, 0)

    def to_prometheus_format(self) -> str:
        """转换为 Prometheus 格式"""
        lines = [f"# HELP {self.name} {self.description}",
                 f"# TYPE {self.name} counter"]
        for key, value in self._values.items():
            if self.labels:
                label_str = ",".join(f'{l}="{v}"' for l, v in zip(self.labels, key))
                lines.append(f"{self.name}{{{label_str}}} {value}")
            else:
                lines.append(f"{self.name} {value}")
        return "\n".join(lines)


class Gauge:
    """仪表"""

    def __init__(self, name: str, description: str = "", labels: List[str] = None):
        self.name = name
        self.description = description
        self.labels = labels or []
        self._values: Dict[tuple, float] = defaultdict(float)

    def set(self, value: float, **label_values):
        """设置值"""
        key = self._get_label_key(label_values)
        self._values[key] = value

    def inc(self, value: float = 1, **label_values):
        """增加"""
        key = self._get_label_key(label_values)
        self._values[key] += value

    def dec(self, value: float = 1, **label_values):
        """减少"""
        key = self._get_label_key(label_values)
        self._values[key] -= value

    def _get_label_key(self, label_values: Dict) -> tuple:
        return tuple(label_values.get(l, "") for l in self.labels)

    def to_prometheus_format(self) -> str:
        """转换为 Prometheus 格式"""
        lines = [f"# HELP {self.name} {self.description}",
                 f"# TYPE {self.name} gauge"]
        for key, value in self._values.items():
            if self.labels:
                label_str = ",".join(f'{l}="{v}"' for l, v in zip(self.labels, key))
                lines.append(f"{self.name}{{{label_str}}} {value}")
            else:
                lines.append(f"{self.name} {value}")
        return "\n".join(lines)


class Histogram:
    """直方图"""

    def __init__(self, name: str, description: str = "", buckets: List[float] = None, labels: List[str] = None):
        self.name = name
        self.description = description
        self.buckets = buckets or [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
        self.labels = labels or []
        self._values: Dict[tuple, List[float]] = defaultdict(list)

    def observe(self, value: float, **label_values):
        """记录观察值"""
        key = self._get_label_key(label_values)
        self._values[key].append(value)

    def _get_label_key(self, label_values: Dict) -> tuple:
        return tuple(label_values.get(l, "") for l in self.labels)

    def to_prometheus_format(self) -> str:
        """转换为 Prometheus 格式"""
        lines = [f"# HELP {self.name} {self.description}",
                 f"# TYPE {self.name} histogram"]
        for key, values in self._values.items():
            if not values:
                continue
            values_sorted = sorted(values)
            total = len(values_sorted)
            cumsum = 0
            for bucket in self.buckets:
                cumsum = sum(1 for v in values_sorted if v <= bucket)
                if self.labels:
                    label_str = ",".join(f'{l}="{v}"' for l, v in zip(self.labels, key))
                    lines.append(f"{self.name}_bucket{{le=\"{bucket}\",{label_str}}} {cumsum}")
                else:
                    lines.append(f"{self.name}_bucket{{le=\"{bucket}\"}} {cumsum}")
            if self.labels:
                label_str = ",".join(f'{l}="{v}"' for l, v in zip(self.labels, key))
                lines.append(f"{self.name}_sum{{{label_str}}} {sum(values_sorted)}")
                lines.append(f"{self.name}_count{{{label_str}}} {total}")
            else:
                lines.append(f"{self.name}_sum {sum(values_sorted)}")
                lines.append(f"{self.name}_count {total}")
        return "\n".join(lines)


class DeleteMetrics:
    """
    删除服务指标收集器

    收集以下指标：
    - delete_requests_total: 删除请求总数
    - delete_duration_seconds: 删除耗时
    - delete_errors_total: 删除错误数
    - active_deletes: 当前活跃删除数
    """

    def __init__(self):
        self.delete_requests = Counter(
            "delete_requests_total",
            "Total delete requests",
            ["delete_type", "status"]
        )
        self.delete_duration = Histogram(
            "delete_duration_seconds",
            "Delete operation duration",
            buckets=[0.01, 0.05, 0.1, 0.5, 1, 5, 10]
        )
        self.delete_errors = Counter(
            "delete_errors_total",
            "Total delete errors",
            ["error_type"]
        )
        self.active_deletes = Gauge(
            "active_deletes",
            "Number of active delete operations"
        )

    def record_delete_request(self, delete_type: str, status: str):
        """记录删除请求"""
        self.delete_requests.inc(delete_type=delete_type, status=status)

    def record_delete_duration(self, duration: float):
        """记录删除耗时"""
        self.delete_duration.observe(duration)

    def record_delete_error(self, error_type: str):
        """记录删除错误"""
        self.delete_errors.inc(error_type=error_type)

    def inc_active_deletes(self):
        """增加活跃删除数"""
        self.active_deletes.inc()

    def dec_active_deletes(self):
        """减少活跃删除数"""
        self.active_deletes.dec()

    def to_prometheus_format(self) -> str:
        """导出 Prometheus 格式"""
        parts = [
            self.delete_requests.to_prometheus_format(),
            self.delete_duration.to_prometheus_format(),
            self.delete_errors.to_prometheus_format(),
            self.active_deletes.to_prometheus_format()
        ]
        return "\n\n".join(filter(None, parts))
