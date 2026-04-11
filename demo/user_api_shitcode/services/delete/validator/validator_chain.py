"""
删除验证器链
"""


class DeleteValidatorChain:
    """删除验证器链"""

    def __init__(self):
        self.validators = []

    def add_validator(self, validator):
        """添加验证器"""
        self.validators.append(validator)

    def validate(self, context):
        """执行验证"""
        for validator in self.validators:
            if not validator.validate(context):
                return False
        return True


class YonghuExistsValidator:
    """用户存在验证器"""

    def validate(self, context):
        """验证用户是否存在"""
        from database_config import get_database
        db = get_database()
        sql = "SELECT COUNT(*) as cnt FROM yonghu WHERE id=" + str(context.yonghu_id)
        result = db.execute(sql).fetchone()
        from database_config import close_database
        close_database(db)

        if result["cnt"] == 0:
            context.add_error("yonghu not exists")
            return False
        return True


class YonghuStatusValidator:
    """用户状态验证器"""

    def validate(self, context):
        """验证用户状态"""
        if context.yonghu_status == "3":
            context.add_error("yonghu already deleted")
            return False
        return True
