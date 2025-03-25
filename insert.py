from app import db, app
from app.models import User, Vote, Ballot, Candidate, Election

with app.app_context():
    vote = Vote.query.all()
    print(vote)