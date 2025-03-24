from app import db, app
from app.models import User, Vote, Ballot, Candidate, Election

with app.app_context():
    ballots = Ballot.query.filter(Ballot.election_id == 2).all()
    for ballot in ballots:
        ballot.status = False
    db.session.commit()