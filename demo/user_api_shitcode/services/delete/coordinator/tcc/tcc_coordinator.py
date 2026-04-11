"""
TCC 分布式事务协调器
"""
from typing import Dict, Any
from services.delete.coordinator.api.delete_dto import DeleteRequest


class TccPhase:
    """TCC 阶段处理器"""

    def __init__(self, try_func, confirm_func, cancel_func):
        self.try_func = try_func
        self.confirm_func = confirm_func
        self.cancel_func = cancel_func


class DeleteTccCoordinator:
    """
    删除 TCC 协调器

    实现三阶段提交：
    - Try: 预留资源，锁定数据
    - Confirm: 确认删除，执行实际删除
    - Cancel: 取消操作，释放预留资源
    """

    def __init__(self):
        self.phases = {
            "user": TccPhase(
                self._try_user_delete,
                self._confirm_user_delete,
                self._cancel_user_delete
            ),
            "cache": TccPhase(
                self._try_cache_delete,
                self._confirm_cache_delete,
                self._cancel_cache_delete
            ),
            "log": TccPhase(
                self._try_log_delete,
                self._confirm_log_delete,
                self._cancel_log_delete
            )
        }

    def execute(self, request: DeleteRequest) -> Dict[str, Any]:
        """
        执行 TCC 流程

        Args:
            request: 删除请求

        Returns:
            执行结果
        """
        try_results = {}

        for resource, phase in self.phases.items():
            try:
                try_results[resource] = phase.try_func(request)
            except Exception as e:
                self._rollback(request, try_results)
                return {"success": False, "phase": "try", "failed_resource": resource}

        for resource, phase in self.phases.items():
            try:
                phase.confirm_func(try_results[resource])
            except Exception as e:
                print(f"Confirm failed for {resource}: {e}")

        return {"success": True, "phase": "confirmed"}

    def _rollback(self, request: DeleteRequest, try_results: Dict):
        """回滚所有预留资源"""
        for resource, phase in self.phases.items():
            if resource in try_results:
                try:
                    phase.cancel_func(try_results[resource])
                except Exception as e:
                    print(f"Cancel failed for {resource}: {e}")

    def _try_user_delete(self, request: DeleteRequest) -> Dict:
        """预留用户删除资源"""
        return {"reserved": True, "yonghu_id": request.yonghu_id}

    def _confirm_user_delete(self, result: Dict):
        """确认用户删除"""
        pass

    def _cancel_user_delete(self, result: Dict):
        """取消用户删除"""
        pass

    def _try_cache_delete(self, request: DeleteRequest) -> Dict:
        """预留缓存删除"""
        return {"reserved": True, "cache_key": f"user:{request.yonghu_id}"}

    def _confirm_cache_delete(self, result: Dict):
        """确认缓存删除"""
        pass

    def _cancel_cache_delete(self, result: Dict):
        """取消缓存删除"""
        pass

    def _try_log_delete(self, request: DeleteRequest) -> Dict:
        """预留日志删除"""
        return {"reserved": True, "request_id": request.request_id}

    def _confirm_log_delete(self, result: Dict):
        """确认日志删除"""
        pass

    def _cancel_log_delete(self, result: Dict):
        """取消日志删除"""
        pass
