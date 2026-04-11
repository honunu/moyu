"""
告警管理器
"""
from typing import Dict, List, Any, Callable
from enum import Enum


class AlertLevel(Enum):
    """告警级别"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Alert:
    """告警"""

    def __init__(self, level: AlertLevel, title: str, message: str, metadata: Dict = None):
        self.level = level
        self.title = title
        self.message = message
        self.metadata = metadata or {}
        self.timestamp = None

    def to_dict(self) -> Dict:
        return {
            "level": self.level.value,
            "title": self.title,
            "message": self.message,
            "metadata": self.metadata
        }


class AlertRule:
    """告警规则"""

    def __init__(self, name: str, condition: Callable[[Dict], bool], level: AlertLevel, message: str):
        self.name = name
        self.condition = condition
        self.level = level
        self.message = message
        self.enabled = True

    def evaluate(self, metrics: Dict) -> bool:
        """评估规则"""
        if not self.enabled:
            return False
        return self.condition(metrics)


class AlertManager:
    """
    告警管理器

    支持：
    - 规则配置
    - 告警触发
    - 告警通知
    """

    def __init__(self):
        self.rules: List[AlertRule] = []
        self.alert_history: List[Alert] = []
        self.handlers: Dict[AlertLevel, List[Callable]] = {
            AlertLevel.INFO: [],
            AlertLevel.WARNING: [],
            AlertLevel.ERROR: [],
            AlertLevel.CRITICAL: []
        }

    def add_rule(self, rule: AlertRule):
        """添加规则"""
        self.rules.append(rule)

    def remove_rule(self, rule_name: str):
        """移除规则"""
        self.rules = [r for r in self.rules if r.name != rule_name]

    def register_handler(self, level: AlertLevel, handler: Callable):
        """注册处理器"""
        self.handlers[level].append(handler)

    def check_metrics(self, metrics: Dict):
        """检查指标"""
        for rule in self.rules:
            if rule.evaluate(metrics):
                alert = Alert(rule.level, rule.name, rule.message, metrics)
                self.send_alert(alert)

    def send_alert(self, alert: Alert):
        """发送告警"""
        self.alert_history.append(alert)
        handlers = self.handlers.get(alert.level, [])
        for handler in handlers:
            try:
                handler(alert)
            except Exception as e:
                print(f"Alert handler error: {e}")

    def get_alert_history(self, level: AlertLevel = None, limit: int = 100) -> List[Alert]:
        """获取告警历史"""
        alerts = self.alert_history
        if level:
            alerts = [a for a in alerts if a.level == level]
        return alerts[-limit:]

    def clear_history(self):
        """清空历史"""
        self.alert_history.clear()
