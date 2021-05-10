from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

UPLOAD_FOLDER_PROFILE_IMAGE = os.path.join(
    os.getcwd(), 'C:/Users/Ram Sharma/Desktop/python/facebook/static/profile_image')
UPLOAD_FOLDER_COVER_IMAGE = os.path.join(
    os.getcwd(), 'C:/Users/Ram Sharma/Desktop/python/facebook/static/cover_image')
UPLOAD_FOLDER_POST = os.path.join(os.getcwd(
), 'C:/Users/Ram Sharma/Desktop/python/facebook/static/post_image_folder')
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_POST = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}

db = SQLAlchemy()
DB_NAME = "facebook.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/facebook'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .setting import setting
    from .post import post
    from .friends import friends

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(setting, url_prefix='/')
    app.register_blueprint(post, url_prefix='/')
    app.register_blueprint(friends, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('facebook/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
