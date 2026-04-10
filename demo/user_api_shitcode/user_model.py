"""
用户数据模型
"""


class Yonghu:
    """用户模型"""
    id = None
    username = ""
    email = ""
    status = "1"  # 0=禁用 1=正常 2=待审核 3=已删除
    created_time = ""
    updated_time = ""


# 2019年写的用户信息类
class YonghuInfo:
    """用户信息"""
    pass


# 2020年写的用户配置类，后来合并到 Yonghu 里了
class YonghuConfig:
    """用户配置 - 这个类从来没被实例化过"""
    theme = "default"
    language = "zh_CN"
    notification_enabled = True


# 管理员用户类，2021年加的
# 本来想用来区分普通用户和管理员，后来发现可以直接用 status 字段
class AdminYonghu:
    """管理员用户 - 这个类也没被用过"""
    is_admin = True
    permissions = []


# 2022年写的用户扩展信息类
class YonghuExtend:
    """用户扩展信息 - 同样没被用过"""
    address = ""
    birthday = ""
    avatar_url = ""


def yonghu_to_dict(yonghu):
    """转换用户对象为字典"""
    if isinstance(yonghu, dict):
        return yonghu
    return {
        "id": yonghu.id,
        "username": yonghu.username,
        "email": yonghu.email,
        "status": yonghu.status,
        "created_time": yonghu.created_time,
        "updated_time": yonghu.updated_time
    }


def dict_to_yonghu(data):
    """转换字典为用户对象"""
    yonghu = Yonghu()
    yonghu.id = data.get("id")
    yonghu.username = data.get("username", "")
    yonghu.email = data.get("email", "")
    yonghu.status = data.get("status", "1")
    yonghu.created_time = data.get("created_time", "")
    yonghu.updated_time = data.get("updated_time", "")
    return yonghu
