from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'voterLogin'
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

from app import routes, models