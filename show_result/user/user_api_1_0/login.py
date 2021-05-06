from flask import jsonify, session, request, current_app
from show_result.model import User
from show_result import db

from . import api

# @api.route('/register', methods=["GET"])
# def register():
#     """用户注册"""
#     name = request.args.get("username")
#     password = request.args.get("password")
#
#     user = User(name=name, password=password)
#     db.session.add(user)
#     db.session.commit()
#     return "ok"

@api.route('/login', methods=["POST"])
def login():
    # 用户登陆模块
    # 1、获取参数
    req_dict = request.get_json()
    username = req_dict.get('username')
    password = req_dict.get('password')

    # 2、校验参数
    if not all([username, password]):
        return jsonify(errno=0, errmsg="参数不完整")

    # 3、从数据库中获取密码与用户填写的密码进行比较
    try:
        user = User.query.filter_by(name=username).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=1, errmsg="获取用户信息失败")

    if user is None or not user.check_password(password):
        return jsonify(errno=2, errmsg="用户名不存在或密码错误")

    # 4、如果验证成功，保存登陆状态，在session
    session["name"] = user.name
    session["user_id"] = user.id

    return jsonify(errno=3, errmsg="登陆成功")

@api.route('/session', methods=["GET"])
def check_login():
    """检查用户登陆状态"""
    # 1、尝试从session中获取用户的名字
    name = session.get("name")
    # 2、如果session中数据name名字存在，则表示用户已经登陆，否则未登录
    if name is not None:
        return jsonify(errno=0, errmsg="用户已经登陆", data={"name": name, "sign": 1})
    else:
        return jsonify(errno=1, errmsg="用户未登录", data={"sign": 0})

@api.route('/session', methods=["DELETE"])
def logout():
    """退出登陆"""
    session.clear()
    return jsonify(errno=0, errmsg="OK")