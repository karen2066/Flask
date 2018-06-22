import os
from flask import Blueprint, render_template, jsonify, request, session

from App.models import Area, Facility, House, db, HouseImage
from utils import status_code
from utils.setting import UPLOAD_DIR

house_blueprint = Blueprint('house', __name__)


# 我的房源页面
@house_blueprint.route('/myhouse/', methods=['GET'])
def my_house():
    return render_template('myhouse.html')


# 返回我的房源数据
@house_blueprint.route('/myhouses/', methods=['GET'])
def user_my_house():
    houses = House.query.filter(House.user_id == session['user_id']).all()
    houses_info = [house.to_dict() for house in houses]
    return jsonify(code=status_code.ok, houses=houses_info)


# 访问发布房源的页面
@house_blueprint.route('/newhouse/', methods=['GET'])
def new_house():
    return render_template('newhouse.html')


# 获取区域和设备的信息（查询接口）
@house_blueprint.route('/area_facility/', methods=['GET'])
def area_facility():
    # 拿到地区和设备的列表
    areas = Area.query.all()
    facilitys = Facility.query.all()

    # 序列化处理每一个地区和设备
    area_list = [area.to_dict() for area in areas]
    facilitys_list = [facility.to_dict() for facility in facilitys]

    # 返回状态码，地区列表和设备列表
    return jsonify(code=status_code.ok,
                   areas=area_list,
                   facilitys=facilitys_list
                   )


# 发布新房源
@house_blueprint.route('/newhouse/', methods=['POST'])
def user_new_house():
    data = request.form.to_dict()
    facility_ids = request.form.getlist('facility')

    house = House()
    house.user_id = session['user_id']
    house.title = data.get('title')
    house.price = data.get('price')
    house.area_id = data.get('area_id')
    house.address = data.get('address')
    house.room_count = data.get('room_count')
    house.house_id = data.get('acreage')
    house.unit = data.get('unit')
    house.capacity = data.get('capacity')
    house.beds = data.get('beds')
    house.deposit = data.get('deposit')
    house.min_days = data.get('min_days')
    house.max_days = data.get('max_days')

    facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
    house.facilities = facility_list
    try:
        house.add_update()
    except:
        db.session.rollback()
    return jsonify(code=status_code.ok, house_id=house.id)


# 保存房屋图片
@house_blueprint.route('/house_images/', methods=['POST'])
def house_images():
    house_id = request.form.get('house_id')
    house_image = request.files.get('house_image')

    save_url = os.path.join(UPLOAD_DIR, house_image.filename)
    house_image.save(save_url)

    # 保存房屋图片信息
    image_url = os.path.join('upload', house_image.filename)

    # 保存房屋的首图
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = image_url
        house.add_update()

    h_image = HouseImage()
    h_image.house_id = house_id
    h_image.url = image_url
    try:
        h_image.add_update()
    except:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify(code=status_code.ok, image_url=image_url)


# 展示详细房屋信息页面
@house_blueprint.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@house_blueprint.route('/detail/<int:id>/', methods=['GET'])
def house_detail(id):
    house = House.query.get(id)
    house_info = house.to_full_dict()

    return jsonify(code=status_code.ok,
                   house_info=house_info)


# 创建预约单
@house_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')
