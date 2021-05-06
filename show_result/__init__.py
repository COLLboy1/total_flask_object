from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
import flask_wtf
import logging
import redis

from logging.handlers import RotatingFileHandler

from show_result.utils.commons import ReConverter

# 创建数据库对象
db = SQLAlchemy()

# 设置日志的的登记
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器，设置日志的保存路径和每个日志的大小和日志的总大小
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录格式，日志等级，输出日志的文件名 行数 日志信息
formatter = logging.Formatter("%(levelname)s %(filename)s: %(lineno)d %(message)s")
# 为日志记录器设置记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flaks app使用的）加载日志记录器
logging.getLogger().addHandler(file_log_handler)

# 创建redis链接对象
redis_store = None

# 工厂模式
def create_app(config_name):
    """
    创建flask的应用对象
    :param config_name:
    """
    app = Flask(__name__)
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 数据库
    db.init_app(app)

    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 对flask补充csrf防护
    flask_wtf.CSRFProtect(app)

    # 为flask添加自定义的转换器,,
    app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    from show_result.lianjia_spyder import lianjia_api_1_0
    app.register_blueprint(lianjia_api_1_0.api, url_prefix="/api/v1.0/lianjia")

    from show_result.user import user_api_1_0
    app.register_blueprint(user_api_1_0.api, url_prefix="/api/v1.0/user")

    # 注册提供静态文件的蓝图
    from show_result import web_html
    app.register_blueprint(web_html.html)

    return app