from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
import functools

# 定义正则转换器
class ReConverter(BaseConverter):
    """"""
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex


# 定义验证登陆状态的装饰器
def login_required(view_fun):
    @functools.wraps(view_fun)
    def wrapper(*args, **kwargs):
        # 判断用户的登陆状态
        user_id = session.get("user_id")
        # 如果用户登陆，执行视图函数
        if user_id is not None:
            # 将user_id保存到g对象中，在视图函数中可以通过g对象获取保存数据
            g.user_id = user_id
            return view_fun(*args, **kwargs)
        # 如果登陆失败
        else:
            return jsonify(errno=-1, errmsg="用户未登录")
    return wrapper