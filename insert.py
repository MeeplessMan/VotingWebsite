from app import db, app
from app.models import User

with app.app_context():
    u = User(email="mprevani2@gmail.com", campus="Durban", role="student")
    u.set_password("password")
    db.session.add(u)
    db.session.commit()
    print(u)
