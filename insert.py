from app import db, app
from app.models import User

with app.app_context():
    u = User(email="22382901@dut4life.ac.za", campus="Durban", role="admin")
    u.set_password("password")
    db.session.add(u)
    db.session.commit()
    print(u)
