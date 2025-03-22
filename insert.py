from app import db, app
from app.models import User

with app.app_context():
    u = User.query.filter_by(email='ateshreddy@gmail.com').first()
    u.role = 'admin'
    db.session.commit()
    print(u.role)
