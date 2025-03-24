from datetime import datetime
from app import db, login
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

default_password = generate_password_hash('password')

class User(UserMixin, db.Model):
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    fullname = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False, default= default_password)
    campus = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    votes = db.relationship('Vote', backref='user', lazy=True)
    registered = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        return self.role == role

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #encrypted_vote_data = db.Column(db.String(100), nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.now)
    ballot_id = db.Column(db.Integer, db.ForeignKey('ballot.id', name='fk_vote_ballot'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_vote_user'), nullable=False)

    def __repr__(self):
        return '<Vote {}>'.format(self.id)
    
class Ballot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campus = db.Column(db.String(20), nullable=False)
    selections = db.Column(db.Integer, nullable=False)
    #voting_options = db.Column(db.String(80), nullable=False) # not needed
    votes = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Boolean, nullable=False, default=False)
    candidates = db.relationship('Candidate', backref='ballot', lazy=True)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id', name='fk_ballot_election'), nullable=False)

    def __repr__(self):
        return '<Ballot {}>'.format(self.id)
   
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(45), nullable=False)
    manifesto = db.Column(db.String(1000), nullable=False)
    campus = db.Column(db.String(45), nullable=False)
    number_votes = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    ballot_id = db.Column(db.Integer, db.ForeignKey('ballot.id', name='fk_candidate_ballot'), nullable=False)

    def __repr__(self):
        return '<Candidate {}>'.format(self.candidate_id)

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_name = db.Column(db.String(45), nullable
= False)
    start_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime, default=datetime.now)
    election_status = db.Column(db.String(20), nullable=False) 
    ballot = db.relationship('Ballot', backref='election', lazy=True)

    def __repr__(self):
        return '<Election {}>'.format(self.id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))