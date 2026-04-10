"""
用户服务层
业务逻辑处理
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model.user import User
from schema.user_schema import UserCreate, UserUpdate
import logging

logger = logging.getLogger(__name__)


class UserService:
    """用户服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: UserCreate) -> User:
        """创建用户"""
        user = User(**user_data.model_dump())
        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("用户名或邮箱已存在")

    def get(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100, status: Optional[int] = None) -> List[User]:
        """获取用户列表"""
        query = self.db.query(User)
        if status is not None:
            query = query.filter(User.status == status)
        return query.offset(skip).limit(limit).all()

    def count(self, status: Optional[int] = None) -> int:
        """统计用户数量"""
        query = self.db.query(User)
        if status is not None:
            query = query.filter(User.status == status)
        return query.count()

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """更新用户"""
        user = self.get(user_id)
        if not user:
            return None
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("用户名或邮箱已存在")

    def delete(self, user_id: int) -> bool:
        """删除用户"""
        user = self.get(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
