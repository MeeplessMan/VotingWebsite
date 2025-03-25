from app import db, app
from app.models import User, Vote, Ballot, Candidate, Election

with app.app_context():
    vote = Vote.query.all()
    for v in vote:
        db.session.delete(v)
    db.session.commit()
    print(vote)