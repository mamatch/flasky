from ensurepip import bootstrap
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config


db = SQLAlchemy()
boots = Bootstrap()
mail = Mail()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    boots.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    # Attach routes and custom error pages here
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
