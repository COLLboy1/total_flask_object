from flask import Blueprint

# 创建蓝图
api = Blueprint("user01_api_1_0",
                __name__,
                )

from . import login