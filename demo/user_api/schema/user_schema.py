"""
用户数据模式定义
Pydantic 模型用于请求验证
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模式"""
    username: str = Field(..., min_length=2, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    status: int = Field(1, ge=0, le=1, description="状态 1:启用 0:禁用")


class UserCreate(UserBase):
    """创建用户请求模式"""
    pass


class UserUpdate(BaseModel):
    """更新用户请求模式"""
    username: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    status: Optional[int] = Field(None, ge=0, le=1)


class UserResponse(UserBase):
    """用户响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """用户列表响应模式"""
    total: int
    users: List[UserResponse]
