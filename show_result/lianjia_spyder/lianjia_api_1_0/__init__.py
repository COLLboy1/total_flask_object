from flask import Blueprint

# 创建蓝图
api = Blueprint("lianjia_api_1_0",
                __name__,
                url_prefix='/lianjia',
                static_folder='lianjia_static'
                )

# 导入蓝图的视图
from . import lianjia