from . import api
from show_result.model import User
from show_result.lianjia_spyder.models import Lianjia_city_info, Lianjia_village_info, Lianjia_village_price_info, Lianjia_village_data_info
from flask import make_response, g, request, session, jsonify, send_from_directory

from werkzeug.utils import secure_filename
from show_result.utils.read_excel import read_data
from show_result import db

import os

from show_result.utils.commons import login_required


# @api.route('/city', methods=["GET"])
# def city():
#     city = request.args.get("city")
#     lianjia_city = Lianjia_city_info(city_name=city)
#     db.session.add(lianjia_city)
#     db.session.commit()
#     return "ok"

# 更新日期信息
# @api.route('/data', methods=['GET'])
# def get_data():
#     year = request.args.get("year")
#     month = request.args.get("month")
#
#     data_info = Lianjia_village_data_info(
#         year=year,
#         month=month
#     )
#
#     db.session.add(data_info)
#     db.session.commit()
#     return "ok"

#######################  数据查询功能  ########################
@api.route('/lianjia_city', methods=["GET"])
def get_city():
    """获取城市信息"""
    city_lists = []
    # 1、判断用户是否登陆

    # 2、查询数据
    try:
        citys = Lianjia_city_info.query.all()
        for city in citys:
            city_data = {
                "city_id": city.id,
                "city_name": city.city_name
            }
            city_lists.append(city_data)
    except Exception as e:
        print(e)
        return jsonify(errno=0, errmsg="数据库查询失败")

    # 3、反回数据
    return jsonify(errno=1, errmsg="OK", city_data=city_lists)

@api.route('/lianjia_village', methods=["GET"])
@login_required
def get_lianjia_village():
    """获取链家小区详细信息"""
    # 1、判断用户是否登陆
    user_id = g.user_id
    if user_id is None:
        return jsonify(errno=0, errmsg="请登录")

    # 设置全局参数
    lianjia_village_lists = []

    # 2、获取参数
    city_id = request.args.get('city_id')
    year = request.args.get('year')
    month = request.args.get('month')
    page = request.args.get('page')

    if not all([city_id]):
        return jsonify(errno=1, errmsg="数据不完整")

    # 3、根据数据进行查询
    try:
        lianjia_villages = Lianjia_village_info.query.filter_by(city_id=city_id)

        total_page = int(len(list(lianjia_villages)) / 20) + 1

        if page is not None:
            now_page = page
            if total_page != page:
                start = (int(page) -1) * 20
                end = int(page) * 20
            else:
                start = (int(page) -1) * 20
                end = -1
        else:
            now_page = 1
            start = 1
            end = 20

        for lianjia_village in lianjia_villages[start: end]:
            lianjia_village_id = lianjia_village.id

            lianjia_village_data_dict = {
                "village_id": lianjia_village.id,
                "village_name": lianjia_village.village_name,
                "village_addr": lianjia_village.village_addr,
                "village_detail_addr": lianjia_village.village_detail_addr,
                "village_year": lianjia_village.village_year,
                "village_building_type": lianjia_village.village_building_type,
                "village_developer": lianjia_village.village_developer,
                "village_property_charges_min": lianjia_village.village_property_charges_min,
                "village_property_charges_max": lianjia_village.village_property_charges_max,
                "village_building_blocks_num": lianjia_village.village_building_blocks_num,
                "village_door": lianjia_village.village_door,
                "village_longitude": lianjia_village.village_longitude,
                "village_latitude": lianjia_village.village_latitude,
                "village_sale_num": lianjia_village.village_sale_num,
                "village_access_rate": lianjia_village.village_access_rate,
                "village_green_rate": lianjia_village.village_green_rate,
                "village_plot_ratio": lianjia_village.village_plot_ratio,
                "village_score": lianjia_village.village_score,
                "traffic_name_info": lianjia_village.traffic_name_info,
                "traffic_distance_info": lianjia_village.traffic_distance_info,
                "hospital_name_info": lianjia_village.hospital_name_info,
                "hospital_distance_info": lianjia_village.hospital_distance_info,
                "park_name_info": lianjia_village.park_name_info,
                "park_distance_info": lianjia_village.park_distance_info,
                "market_name_info": lianjia_village.market_name_info,
                "market_distance_info": lianjia_village.market_distance_info
            }

            lianjia_village_lists.append(lianjia_village_data_dict)
    except Exception as e:
        print(e)
        return jsonify(errno=2, errmsg="未查到相关数据")

    # 4、返回数据
    return jsonify(errno=3, errmsg="查询成功", data=lianjia_village_lists, total_page=total_page, now_page=now_page)

@api.route('/lianjia_data', methods=['GET'])
def get_lianjia_data_village():
    """获取日期信息"""
    year_lists = []
    month_lists = []
    #1、查找所有日期信息
    try:
        lianjia_data_info = Lianjia_village_data_info.query.all()
        for lianjia_data in lianjia_data_info:
            year = lianjia_data.year

            month = lianjia_data.month
            if year not in year_lists:
                year_lists.append(year)
            if month not in month_lists:
                month_lists.append(month)

    except Exception as e:
        return jsonify(errno=0, errmsg="数据查询失败")

    return jsonify(errno=1, errmsg="OK", month_lists=month_lists, year_lists=year_lists)

#######################  上传/下载功能 ########################
progress_data = {}

@api.route('/save_data', methods=["POST"])
@login_required
def save_data():
    """保存上传的文件"""
    # 1、判断用户是否登陆
    user_id = g.user_id
    if user_id is None:
        return jsonify(errno=0, errmsg="用户未登录")

    # 2、获取表单数据
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        if filename.split(".")[1].lower() != "csv":
            return jsonify(errno=1, errmsg="数据格式不正确")

        # 判断文件是否已经导入
        file_list = os.listdir(os.getcwd() + '/show_result/static/lianjia_data/')

        if filename in file_list:
            return jsonify(errno=2, errmsg="文件重复导入")
        # 保存文件路径
        file_path = os.getcwd() + '/show_result/static/lianjia_data/' + filename
        # 保存文件
        file.save(file_path)
    else:
        return jsonify(errno=3, errmsg="请选择文件")
    # 3、读取文件内容并保存到数据库
    data_lists = read_data(file_path)

    # 判断小区的基本信息是否已经导入
    try:
        lianjia_village_info = Lianjia_village_info.query.filter_by(city_id=data_lists[0][1]).first()

        for i in data_lists[0: 10]:
            try:
                # 根据url地址寻找小区的id号
                lianjia_village_id = Lianjia_village_info.query.filter_by(village_url=i[0]).first().id
                try:
                    #根据id号判断 本月的价格是否已经 保存
                    lianjia_price_info = Lianjia_village_price_info.filter_by(village_id=lianjia_village_id, year=i[2], month=i[3]).first()
                    print(lianjia_village_info + "的数据已经存在")
                except Exception as e:
                    lianjia_price = Lianjia_village_price_info(
                        village_id=lianjia_village_id,
                        year=i[2],
                        month=i[3],
                        village_unit_price=i[5]
                    )

                    try:
                        db.session.add(lianjia_price)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
            except Exception as e:
                print(e)

    except Exception as e:
        print("正在保存数据")
        for i in data_lists:
            lianjia_village = Lianjia_village_info(
                city_id=i[1],
                village_url=i[0],
                village_name=i[4],
                village_addr=i[6],
                village_detail_addr=i[7],
                village_year=i[8],
                village_building_type=i[9],
                village_developer=i[10],
                village_property_charges_min=i[11],
                village_property_charges_max=i[12],
                village_building_blocks_num=i[13],
                village_door=i[14],
                village_longitude=i[15],
                village_latitude=i[16],
                village_sale_num=i[17],
                village_access_rate=i[18],
                village_green_rate=i[19],
                village_plot_ratio=i[20],
                village_score=i[21],
                traffic_name_info=i[22],
                traffic_distance_info=i[23],
                hospital_name_info=i[24],
                hospital_distance_info=i[25],
                park_name_info=i[26],
                park_distance_info=i[27],
                market_name_info=i[28],
                market_distance_info=i[29]
            )

            try:
                db.session.add(lianjia_village)
                db.session.commit()

            except Exception as e:
                print(e)
                db.session.rollback()

            # 保存价格信息
            lianjia_village_id = lianjia_village.id

            lianjia_price = Lianjia_village_price_info(
                village_id=lianjia_village_id,
                year=i[2],
                month=i[3],
                village_unit_price=i[5]
            )

            try:
                db.session.add(lianjia_price)
                db.session.commit()
            except Exception as e:
                db.session.rollback()


    return jsonify(errno=4, errmsg="导入成功")

@api.route('/download_data')
@login_required
def download_data():
    # 1、获取参数，查看参数是否完整
    year = request.args.get('year')
    month = request.args.get('month')
    city_id = request.args.get('city_id')

    if not all([year, month, city_id]):
        return  jsonify(errno=0, errmsg="参数不完整")
    # 2、处理简单的业务逻辑
    filepath = os.getcwd() + "/show_result/static/lianjia_data/"
    filename = year + month + city_id + '.csv'

    try:
        return send_from_directory(filepath, filename, as_attachment=True)
    except Exception as e:
        return jsonify(errno=1, errmsg="数据下载失败")
