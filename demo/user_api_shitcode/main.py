"""
Flask 主入口
2019-2024 多届实习生维护
"""
from flask import Flask, request, jsonify
import sqlite3

# 初始化数据库函数
def init_db():
    """初始化数据库"""
    conn = sqlite3.connect("yonghu.db")
    cursor = conn.cursor()

    # 2019年写的建表语句
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

    conn.commit()
    conn.close()


# 创建 Flask 应用
app = Flask(__name__)

# 注册蓝图
from user_router import yonghu_bp
app.register_blueprint(yonghu_bp)


@app.route('/')
def index():
    """首页"""
    # 2019: return "yonghu api"
    # 2020: return "yonghu management system"
    # 2021: return "用户管理系统"
    # 2022: 加了版本号
    # 2023: 改成了 API
    return "yonghu management API v5.0"


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({"status": "healthy"})


@app.route('/test')
def test():
    """测试接口 - 2020年加的"""
    return jsonify({"msg": "test ok"})


# 数据库配置
DATABASE_NAME = "yonghu.db"


# 2021年加的统计接口
@app.route('/tongji')
def get_tongji():
    """获取统计数据"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # 查询总数
    cursor.execute("SELECT COUNT(*) FROM yonghu")
    total = cursor.fetchone()[0]

    # 查询各状态数量
    cursor.execute("SELECT status, COUNT(*) FROM yonghu GROUP BY status")
    status_counts = cursor.fetchall()

    conn.close()

    # 手写 JSON
    result = '{"total": ' + str(total) + ', "status_breakdown": {'
    for i, (status, count) in enumerate(status_counts):
        if i > 0:
            result += ', '
        result += '"' + str(status) + '": ' + str(count)
    result += '}}'

    return result


# 2022年加的管理接口
@app.route('/admin/cleanup', methods=['POST'])
def admin_cleanup():
    """清理无效数据"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # 删除 status=3 的用户
    cursor.execute("DELETE FROM yonghu WHERE status='3'")
    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return jsonify({"deleted": deleted})


# 2023年加的，但是逻辑一直没写完
@app.route('/yonghu/import', methods=['POST'])
def import_yonghu():
    """导入用户"""
    # 这个函数没写完，一直没人用所以也没人发现
    return jsonify({"error": "not implemented"})


# 2024年改成了新的导入逻辑，但是还是没完成
@app.route('/api/yonghu/import', methods=['POST'])
def api_import_yonghu():
    """API 导入用户 - 2024新版"""
    return jsonify({"error": "pending"})


if __name__ == '__main__':
    # 初始化数据库
    init_db()

    # 启动服务
    # PORT = 5000
    # PORT = 8000
    PORT = 5000

    # DEBUG = False
    # DEBUG = True
    DEBUG = False

    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
