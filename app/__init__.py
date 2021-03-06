from config import config_options
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import  configure_uploads, UploadSet, IMAGES
from flask_simplemde import SimpleMDE


db = SQLAlchemy()
bootstrap = Bootstrap()
photos = UploadSet('photos', IMAGES)
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

simple = SimpleMDE()



def create_app(config_name):

    app = Flask(__name__)
    

        # Creating the main configurations
    app.config.from_object(config_options[config_name])
   

    # Initializing flask extensions
    simple.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
    
    # configure UploadSet
    configure_uploads(app,photos)

    return app