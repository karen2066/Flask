# 创建app,配置static和templates
import os

import redis
from flask import Flask
from flask_session import Session

from App.house_views import house_blueprint
from App.models import db
from App.order_views import order_blueprint
from App.user_views import user_blueprint
from utils.setting import BASE_DIR

se = Session()


def create_app():
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')
    app.register_blueprint(blueprint=order_blueprint, url_prefix='/order')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/aj'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS '] = redis.Redis(host='127.0.0.1', port=6379)

    db.init_app(app=app)
    se.init_app(app=app)

    return app


