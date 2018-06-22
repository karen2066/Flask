
from datetime import datetime

from flask import Blueprint, render_template, url_for, \
    session, request, jsonify

from App.models import Order, House
from utils.functions import is_login
from utils import status_code


order_blueprint = Blueprint('order', __name__)


# 创建订单
@order_blueprint.route('/create_order/', methods=['POST'])
def create_order():

    begin_date = datetime.strptime(request.form.get('begin_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    house_id = request.form.get('house_id')
    user_id = session['user_id']

    if not all([begin_date, end_date]):
        return jsonify(status_code.ORDER_BEGIN_END_DATA_NOT_NULL)

    if begin_date > end_date:
        return jsonify(status_code.ORDER_BEGIN_DATA_GT_END_DATE_ERROR)

    house = House.query.get(house_id)

    order = Order()
    order.user_id = user_id
    order.house_id = house_id
    order.begin_date = begin_date
    order.end_date = end_date
    order.days = (end_date - begin_date).days + 1
    order.house_price = house.price
    order.amount = order.days * order.house_price

    order.add_update()

    return jsonify(status_code.success)

