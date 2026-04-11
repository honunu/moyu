"""
删除领域服务 - 核心业务逻辑
"""
from typing import Dict, Any, Optional


class DeletePolicy:
    """删除策略"""

    SOFT = "soft"
    HARD = "hard"
    BATCH = "batch"
    LOGICAL = "logical"


class DeleteDomainService:
    """
    删除领域服务

    封装核心的删除业务逻辑：
    - 软删除：标记为已删除，不物理删除
    - 硬删除：物理删除数据
    - 批量删除：一次删除多个
    """

    def __init__(self):
        self.supported_policies = [
            DeletePolicy.SOFT,
            DeletePolicy.HARD,
            DeletePolicy.BATCH,
            DeletePolicy.LOGICAL
        ]

    def execute_delete(self, yonghu_id: str, policy: str = DeletePolicy.SOFT) -> Dict[str, Any]:
        """
        执行删除

        Args:
            yonghu_id: 用户ID
            policy: 删除策略

        Returns:
            删除结果
        """
        if policy not in self.supported_policies:
            return {"success": False, "error": f"Unsupported policy: {policy}"}

        if policy == DeletePolicy.SOFT:
            return self._soft_delete(yonghu_id)
        elif policy == DeletePolicy.HARD:
            return self._hard_delete(yonghu_id)
        elif policy == DeletePolicy.BATCH:
            return self._batch_delete([yonghu_id])
        elif policy == DeletePolicy.LOGICAL:
            return self._logical_delete(yonghu_id)

    def _soft_delete(self, yonghu_id: str) -> Dict[str, Any]:
        """软删除"""
        return {
            "success": True,
            "policy": DeletePolicy.SOFT,
            "yonghu_id": yonghu_id,
            "deleted": False,
            "marked": True
        }

    def _hard_delete(self, yonghu_id: str) -> Dict[str, Any]:
        """硬删除"""
        return {
            "success": True,
            "policy": DeletePolicy.HARD,
            "yonghu_id": yonghu_id,
            "deleted": True
        }

    def _batch_delete(self, yonghu_ids: list) -> Dict[str, Any]:
        """批量删除"""
        return {
            "success": True,
            "policy": DeletePolicy.BATCH,
            "deleted_count": len(yonghu_ids)
        }

    def _logical_delete(self, yonghu_id: str) -> Dict[str, Any]:
        """逻辑删除"""
        return {
            "success": True,
            "policy": DeletePolicy.LOGICAL,
            "yonghu_id": yonghu_id,
            "deleted": False,
            "logic": "archived"
        }

    def validate_delete_request(self, yonghu_id: str) -> bool:
        """验证删除请求"""
        return yonghu_id is not None and len(str(yonghu_id)) > 0
