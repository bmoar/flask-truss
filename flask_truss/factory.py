from werkzeug.contrib.fixers import ProxyFix
from celery import Celery
from flask import Flask
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager

from flask_truss.conf.app import Config
from flask_truss.admin import admin_extension
from flask_truss.marshmallow import marshmallow
from flask_truss.models.base import db
from flask_truss.models.user import User, Anonymous
from flask_truss.libs.logger import init_logger


login_manager = LoginManager()
debug_toolbar = DebugToolbarExtension()


def load_user(user_id):
    """Finds and returns a user for flask-login"""
    return User.query.get(int(user_id))


def create_base_app(config):
    """Init configuration and extensions"""
    app = Flask(__name__)
    app.config.from_object(config)
    config.init_app(app)

    app._logger = init_logger(syslogtag=app.config['LOGGER_SYSLOGTAG'],
                              logger_name=app.config['LOGGER_NAME'])

    marshmallow.init_app(app)
    db.init_app(app)

    if app.config['DEBUG']:
        admin_extension.init_app(app)
        debug_toolbar.init_app(app)

    login_manager.init_app(app)
    login_manager.anonymous_user = Anonymous
    # Change these views to fit your app.
    # Use flask_truss.auth.attempt_login to login a user.
    login_manager.login_view = "auth.login"
    login_manager.refresh_view = "auth.login"
    login_manager.login_message = "You do not have access to that page."
    login_manager.user_loader(load_user)

    return app


def create_celery_app():
    """Create and return a celery instance based off of an app or by creating a new app

    The celery instance needs to know the app configuration in order to get the broker_url and other settings.
    """
    app = create_base_app(Config())
    celery_instance = Celery(__name__, broker=Config().BROKER_URL)
    celery_instance.conf.update(app.config)

    return celery_instance


def register_blueprints(app):
    """Import and register blueprints"""
    from flask_truss.blueprints._blueprint import _blueprint
    app.register_blueprint(_blueprint, url_prefix='/')

    return app


def create_app(config):
    """Produce an application ready with all config settings, blueprints, and the ProxyFix"""
    app = create_base_app(config)
    app = register_blueprints(app)
    # Apply the ProxyFix so that requests get the correct headers. Change if not using a proxy.
    # http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/#proxy-setups
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
