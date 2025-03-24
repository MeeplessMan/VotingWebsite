from app import db, app
from app.models import User, Vote, Ballot, Candidate, Election

with app.app_context():
    Election.query.delete()
    Ballot.query.delete()
    db.session.commit()
    print(Election.query.all())