from datetime import datetime

from show_result import db

class BaseModel(object):
    """创建模型基类，为每一个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now())  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())  # 记录更新的时间

class Lianjia_city_info(db.Model):
    """链家城市信息"""
    __tablename__ = "lianjia_city_info"

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(128), nullable=False)

class Lianjia_village_info(db.Model):
    """链家所有小区详细信息"""
    __tablename__ = "lianjia_village_info"
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('lianjia_city_info.id'))
    village_url = db.Column(db.String(300), nullable=False)

    village_name = db.Column(db.String(64), nullable=False)
    village_addr = db.Column(db.String(64), nullable=False)
    village_detail_addr = db.Column(db.String(128), nullable=False)
    village_year = db.Column(db.String(128), nullable=False)
    village_building_type = db.Column(db.String(128), nullable=False)
    village_developer = db.Column(db.String(128), nullable=False)
    village_property_charges_min = db.Column(db.String(128), nullable=False)
    village_property_charges_max = db.Column(db.String(128), nullable=False)
    village_building_blocks_num = db.Column(db.String(128), nullable=False)
    village_door = db.Column(db.String(128), nullable=False)
    village_longitude = db.Column(db.String(128), nullable=False)
    village_latitude = db.Column(db.String(128), nullable=False)

    village_sale_num = db.Column(db.String(32), nullable=False)
    village_access_rate = db.Column(db.String(32), nullable=False)
    village_green_rate = db.Column(db.String(128), nullable=False)
    village_plot_ratio = db.Column(db.String(128), nullable=False)
    village_score = db.Column(db.String(32), nullable=False)

    traffic_name_info = db.Column(db.String(1280), nullable=False)
    traffic_distance_info = db.Column(db.String(1280), nullable=False)
    hospital_name_info = db.Column(db.String(1280), nullable=False)
    hospital_distance_info = db.Column(db.String(1280), nullable=False)
    park_name_info = db.Column(db.String(1280), nullable=False)
    park_distance_info = db.Column(db.String(1280), nullable=False)
    market_name_info = db.Column(db.String(1280), nullable=False)
    market_distance_info = db.Column(db.String(1280), nullable=False)

class Lianjia_village_price_info(db.Model):
    """价格信息"""
    id = db.Column(db.Integer, primary_key=True)
    village_id = db.Column(db.Integer, db.ForeignKey('lianjia_village_info.id'))
    year = db.Column(db.String(128), nullable=False)
    month = db.Column(db.String(128), nullable=False)
    village_unit_price = db.Column(db.String(128), nullable=False)

class Lianjia_village_data_info(db.Model):
    __tablename__ = "lianjia_village_data_info"

    id = db.Column(db.Integer, primary_key=True)

    year = db.Column(db.String(128), nullable=False)
    month = db.Column(db.String(128), nullable=False)
