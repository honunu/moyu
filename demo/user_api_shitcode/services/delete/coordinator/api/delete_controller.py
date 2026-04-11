"""
删除协调控制器
"""
from typing import Optional, Dict, Any
from services.delete.coordinator.saga.saga_orchestrator import DeleteSagaOrchestrator
from services.delete.coordinator.tcc.tcc_coordinator import DeleteTccCoordinator
from services.delete.coordinator.api.delete_dto import DeleteRequest, DeleteResponse


class DeleteCoordinatorController:
    """
    删除协调控制器

    协调多个微服务的删除操作，支持 Saga 和 TCC 两种分布式事务模式
    """

    def __init__(self):
        self.saga_orchestrator = DeleteSagaOrchestrator()
        self.tcc_coordinator = DeleteTccCoordinator()

    def delete_yonghu(self, yonghu_id: str, delete_type: str = "soft") -> Dict[str, Any]:
        """
        协调删除用户

        Args:
            yonghu_id: 用户ID
            delete_type: 删除类型 (soft/hard/batch)

        Returns:
            协调结果
        """
        request = DeleteRequest(yonghu_id, delete_type)

        if delete_type == "batch":
            return self._execute_saga_delete(request)
        else:
            return self._execute_tcc_delete(request)

    def _execute_saga_delete(self, request: DeleteRequest) -> Dict[str, Any]:
        """使用 Saga 模式执行批量删除"""
        result = self.saga_orchestrator.execute(request)
        return {
            "request_id": request.request_id,
            "success": result["success"],
            "steps_completed": result.get("completed_steps", []),
            "steps_compensated": result.get("compensated_steps", [])
        }

    def _execute_tcc_delete(self, request: DeleteRequest) -> Dict[str, Any]:
        """使用 TCC 模式执行删除"""
        result = self.tcc_coordinator.execute(request)
        return {
            "request_id": request.request_id,
            "success": result["success"],
            "phase": result.get("phase", "unknown")
        }

    def query_delete_status(self, request_id: str) -> Dict[str, Any]:
        """查询删除状态"""
        return {
            "request_id": request_id,
            "status": "completed",
            "progress": 100
        }
