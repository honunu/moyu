"""
OpenTelemetry 链路追踪
"""
import uuid
import time
from typing import Dict, List, Optional, Any
from contextvars import ContextVar


trace_context: ContextVar[Optional["Span"]] = ContextVar("trace_context", default=None)


class Span:
    """追踪跨度"""

    def __init__(self, name: str, trace_id: str = None, span_id: str = None):
        self.name = name
        self.trace_id = trace_id or self._generate_id(16)
        self.span_id = span_id or self._generate_id(8)
        self.parent_span_id = None
        self.start_time = int(time.time() * 1000000)
        self.end_time = None
        self.attributes: Dict[str, Any] = {}
        self.events: List[Dict] = []
        self.status = "OK"

    @staticmethod
    def _generate_id(length: int) -> str:
        return uuid.uuid4().hex[:length]

    def set_attribute(self, key: str, value: Any):
        """设置属性"""
        self.attributes[key] = value

    def add_event(self, name: str, attributes: Dict = None):
        """添加事件"""
        self.events.append({
            "name": name,
            "timestamp": int(time.time() * 1000000),
            "attributes": attributes or {}
        })

    def set_status(self, status: str):
        """设置状态"""
        self.status = status

    def finish(self):
        """结束跨度"""
        self.end_time = int(time.time() * 1000000)

    def duration(self) -> int:
        """获取耗时（微秒）"""
        if self.end_time:
            return self.end_time - self.start_time
        return int(time.time() * 1000000) - self.start_time

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "attributes": self.attributes,
            "events": self.events,
            "status": self.status
        }


class Tracer:
    """
    链路追踪器

    支持：
    - 创建跨度
    - 跨度嵌套
    - 上下文传播
    - 采样
    """

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.spans: List[Span] = []

    def start_span(self, name: str, parent: Span = None) -> Span:
        """
        开始新的跨度

        Args:
            name: 跨度名称
            parent: 父跨度

        Returns:
            新跨度
        """
        span = Span(name)
        if parent:
            span.trace_id = parent.trace_id
            span.parent_span_id = parent.span_id
        self.spans.append(span)
        trace_context.set(span)
        return span

    def end_span(self, span: Span):
        """结束跨度"""
        span.finish()

    def get_current_span(self) -> Optional[Span]:
        """获取当前跨度"""
        return trace_context.get()

    def extract_context(self) -> Dict:
        """提取上下文"""
        span = self.get_current_span()
        if span:
            return {
                "trace_id": span.trace_id,
                "span_id": span.span_id
            }
        return {}

    def inject_context(self, context: Dict):
        """注入上下文"""
        pass


class TraceManager:
    """
    追踪管理器

    管理所有追踪器
    """

    def __init__(self):
        self.tracers: Dict[str, Tracer] = {}

    def get_tracer(self, service_name: str) -> Tracer:
        """获取追踪器"""
        if service_name not in self.tracers:
            self.tracers[service_name] = Tracer(service_name)
        return self.tracers[service_name]

    def get_all_spans(self, service_name: str = None) -> List[Span]:
        """获取所有跨度"""
        if service_name:
            tracer = self.tracers.get(service_name)
            return tracer.spans if tracer else []
        spans = []
        for tracer in self.tracers.values():
            spans.extend(tracer.spans)
        return spans

    def clear(self):
        """清空追踪数据"""
        for tracer in self.tracers.values():
            tracer.spans.clear()
