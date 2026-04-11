"""
删除请求 DTO
"""
import uuid
import time
from typing import Optional, Dict, Any


class DeleteRequest:
    """删除请求"""

    def __init__(self, yonghu_id: str, delete_type: str = "soft"):
        self.request_id = str(uuid.uuid4())
        self.yonghu_id = yonghu_id
        self.delete_type = delete_type
        self.timestamp = int(time.time() * 1000)
        self.metadata: Dict[str, Any] = {}


class DeleteResponse:
    """删除响应"""

    def __init__(self, request_id: str, success: bool, message: str = ""):
        self.request_id = request_id
        self.success = success
        self.message = message
        self.timestamp = int(time.time() * 1000)
