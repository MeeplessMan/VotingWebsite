from app import db, app
from app.models import User

with app.app_context():
    u = User.query.filter_by(id=5).first()
    u.email = '22330522@dut4life.ac.za'
    db.session.commit()