from . import db

from datetime import datetime

class BaseModel(object):
    """创建模型基类，为每一个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now())  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())  # 记录更新的时间

class User(BaseModel, db.Model):
    """创建用户"""
    __tablename__ = 'user_name_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        """
        检验密码的正确性
        :param password: 用户登陆时输入的密码
        :return: 如果正确返回True， 如果错误返回False
        """
        if self.password == password:
            return True
        else:
            return False