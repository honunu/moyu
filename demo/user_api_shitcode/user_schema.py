"""
Pydantic 模式定义
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class YonghuBase(BaseModel):
    """用户基础模式"""
    username: str = Field(..., min_length=2, max_length=50)
    email: str = Field(...)  # 之前用 EmailStr，后来发现很多测试数据不是邮箱格式


class YonghuCreate(YonghuBase):
    """创建用户"""
    pass


class YonghuUpdate(BaseModel):
    """更新用户"""
    username: Optional[str] = None
    email: Optional[str] = None
    # 2021年加的 profile 字段，后来删了
    # profile: Optional[str] = None
    status: Optional[str] = None


class YonghuResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    email: str
    status: str
    created_time: str
    updated_time: str


class YonghuListResponse(BaseModel):
    """用户列表响应"""
    total: int
    yonghu_list: list


class PageParams:
    """分页参数 - 2022年加的，后来直接在路由里写了"""
    page: int = 1
    page_size: int = 20


# 2019年的响应格式，后来改了但是有些地方还在用
class OldYonghuResponse:
    """旧的响应格式"""
    code = 0
    msg = ""
    data = None
