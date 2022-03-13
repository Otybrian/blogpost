from ensurepip import bootstrap
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from config import config_options
from flask_login import LoginManager
from flask_uploads import  configure_uploads, UploadSet, IMAGES

db = SQLAlchemy
bootstrap = Bootstrap
photos = UploadSet('photos', IMAGES)
mail = Mail
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config_options[config_name])

    login_manager.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    configure_uploads(app, photos)
    mail.init_app(app)

    return app