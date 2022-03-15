import os

class Config:
    SECRET_KEY = '30011397'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:user@localhost/blogs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'otbrayo@gmail.com'
    MAIL_PASSWORD = 'Year2030#'
    UPLOADED_PHOTOS_DEST ='app/static/photos'

class ProdConfig(Config):

    pass 


class DevConfig(Config):

    DEBUG = True


config_options = {
    'development': DevConfig,
    'production' : ProdConfig
}