from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.init_app(app)

    db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

def create_users():
    db.create_all()

    # Add users
    user = find_or_create_user(u'admin', u'admin', 'Admin', u'admin@example.com')
    db.session.commit()


def find_or_create_user(username, name, password, useremail, role=None):
    """ Find existing user or create new user """
    from .models import users
    user = users.query.filter(users.username == username).first()
    if not user:
        user = users(username=username,
                    name=name,
                    password=password,
                    useremail=useremail,)
                    #active=True)
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user
