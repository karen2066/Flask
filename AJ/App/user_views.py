import re

import os
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from App.models import db, User
from utils import status_code
from utils.functions import is_login
from utils.setting import BASE_DIR, UPLOAD_DIR

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def hello():
    return 'hello world'


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'


# 注册方法
@user_blueprint.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user_blueprint.route('/register/', methods=['POST'])
def user_register():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if not all([mobile, password, password2]):
        return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)
    if not re.match(r'^1[34578]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_IS_NOT_VALID)
    user = User.query.filter(User.phone == mobile).all()
    if user:
        return jsonify(status_code.USER_REGISTER_MOBILE_EXISTS)
    else:
        user = User()
        user.phone = mobile
        user.password = password
        user.name = mobile
        user.add_update()
        return jsonify(status_code.success)


# 登录
@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blueprint.route('/login/', methods=['POST'])
def user_login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    if not all([mobile, password]):
        return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)
    if not re.match(r'^1[34578]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
    user = User.query.filter(User.phone == mobile).first()
    if user:
        if not user.check_pwd(password):
            return jsonify(status_code.USER_LOGIN_PASSWORD_IS_NOT_VALID)
        session['user_id'] = user.id
        return jsonify(status_code.success)
    else:
        return jsonify(status_code.USER_LOGIN_USER_NOT_EXSITS)


# 注销
@user_blueprint.route('/logout/', methods=['GET', 'POST'])
def user_logout():
    # 删除session中的值?
    session.clear()
    return redirect(url_for('user.login'))


# 访问个人中心
@user_blueprint.route('/my/', methods=['GET'])
def my():
    return render_template('my.html')


# GET请求加载修改个人信息页面
@user_blueprint.route('/profile/', methods=['GET'])
def profile():
    return render_template('profile.html')


# 上传图片
@user_blueprint.route('/profile/', methods=['PATCH'])
def user_profile():
    file = request.files.get('avatar')
    # 过滤上传的文件类型
    if not re.match(r'image/.*', file.mimetype):
        return jsonify(status_code.USER_CHANGE_PROFILE_IMAGES)
    # 保存图片到地址
    image_path = os.path.join(UPLOAD_DIR, file.filename)  # 根据图片的名字找到路径
    file.save(image_path)  # 保存图片路径

    user = User.query.get(session['user_id'])  # 从user_id拿到user的对象
    avatar_path = os.path.join('upload', file.filename)  # 根据文件名拿到文件地址
    user.avatar = avatar_path  # 将地址保存到数据库的字段
    # 如果数据库挂了
    try:
        user.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    # 上传成功向页面返回图片
    return jsonify(code=status_code.ok, image_url=avatar_path)


# 修改用户名
@user_blueprint.route('/proname/', methods=['PATCH'])
def user_proname():
    # 从页面拿到name
    name = request.form.get('name')
    # 从数据库查找到user对象
    user = User.query.filter_by(name=name).first()
    if user:
        # 过滤用户名是否重复
        return jsonify(status_code.USER_CHANGE_PRONAME_IS_INVALID)
    else:
        # 没有用户，去拿到user_id， 找到当前用户
        user = User.query.get(session['user_id'])
        user.name = name  # 写入用户名
        try:
            user.add_update()
        except Exception as e:
            db.session.rollback()
            return jsonify(status_code.DATABASE_ERROR)
        # 返回状态码和用户名
        return jsonify(code=status_code.ok, name=name)


# 在个人中心页面显示
@user_blueprint.route('/user/', methods=['GET'])
def user_info():
    user = User.query.get(session['user_id'])
    return jsonify(code=status_code.ok, data=user.to_basic_dict())


# 用户认证页面访问
@user_blueprint.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


# 用户认证方法
@user_blueprint.route('/auth/', methods=['PATCH'])
def user_auth():
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    # 判断数据是否完整
    if not all([real_name, id_card]):
        return jsonify(status_code.USER_AUTH_DATA_IS_NOT_NULL)
    # 判断身份证格式
    if not re.match(r'^[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_AUTH_ID_CARD_IS_NOT_VALID)

    user = User.query.get(session['user_id'])
    user.id_name = real_name
    user.id_card = id_card
    try:
        user.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify(status_code.success)


# 获取用户信息
@user_blueprint.route('/auths/', methods=['GET'])
def user_auths():
    user = User.query.get(session['user_id'])

    return jsonify(code=status_code.ok, data=user.to_auth_dict())


