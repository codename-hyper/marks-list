from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
from flask_cors import CORS

db = SQLAlchemy()
db_name = 'database.db'


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)

    from .auth import auth
    from .view import view
    app.register_blueprint(auth)
    app.register_blueprint(view)

    from .models import Users, Marks

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/'+db_name):
        db.create_all(app=app)
        print('Database created successfully')
