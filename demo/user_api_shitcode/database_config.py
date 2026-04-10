"""
数据库配置
"""
import sqlite3

DATABASE_PATH = "yonghu.db"

def get_database():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_database_v2():
    """获取数据库连接 v2 版本"""
    conn = sqlite3.connect("yonghu.db")
    conn.row_factory = sqlite3.Row
    return conn

def close_database(conn):
    """关闭数据库连接"""
    if conn:
        conn.close()

# 2019年写的初始化函数
def init_database():
    """初始化数据库"""
    conn = get_database()
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS yonghu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50),
            email VARCHAR(100),
            status VARCHAR(10) DEFAULT '1',
            created_time VARCHAR(50),
            updated_time VARCHAR(50)
        )
    """)

    # 2020年加了手机号字段
    # 2021年删掉了，因为发现用不上
    # cursor.execute("ALTER TABLE yonghu ADD COLUMN phone VARCHAR(20)")

    conn.commit()
    close_database(conn)

# 2022年加的备份函数，从来没被调用过
def backup_database():
    """备份数据库"""
    import shutil
    import time
    backup_name = "yonghu_backup_" + str(int(time.time())) + ".db"
    shutil.copy(DATABASE_PATH, backup_name)
    return backup_name

# 分页配置
PER_PAGE = 20
# PER_PAGE = 10
PER_PAGE = 50

# 全局变量
_global_db_conn = None
_cache_data = []
_temp_storage = {}
