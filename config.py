import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asjgkahskgashhg'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir, 'votingWebsite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'live.smtp.mailtrap.io'
    MAIL_PORT = 587
    MAIL_USERNAME = 'api'
    MAIL_PASSWORD = '81b957ce1c0cdae23940ffca05fc9db7'
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = 'hi@demomailtrap.co'