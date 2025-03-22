import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asjgkahskgashhg'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir, 'votingWebsite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.hostinger.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'no-reply@dutsrcelections.site'
    MAIL_PASSWORD = 'NMNRp^1=m3'
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = 'no-reply@dutsrcelections.site'