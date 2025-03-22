from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    campus = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    votes= db.relationship('Vote', backref='user', lazy=True)
    registered = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
        return str(self.user_id)
    
class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    #encrypted_vote_data = db.Column(db.String(100), nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    ballot_id = db.Column(db.Integer, db.ForeignKey('ballot.ballot_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    
class Ballot(db.Model):
    ballot_id = db.Column(db.Integer, primary_key=True)
    candidate_list= db.Column(db.String(225), nullable=False)
    campus= db.Column(db.String(20), nullable=False)
    selections= db.Column(db.Integer, nullable=False)
    status= db.Column(db.Boolean, status=False)
   # voting_options= db.Column(db.String(80), nullable=False)# not needed
    votes= db.Relatioship('Vote', backref='ballot', lazy=True)
    candidates = db.Relationship('Candidate',backref='ballot', lazy=True)
   
class Candidate(db.Model):
    candidate_id=db.Column(db.Integer, primary_key=True)
    candidate_name=db.Column(db.String(45), nullable=False)
    manifesto=db.Column(db.String(1000), nullable=False)
    campus=db.Column(db.String(45), nullable=False)
    number_votes=db.Column(db.Integer, nullable=False)
    ballot_id = db.Column(db.Integer, db.ForeignKey('ballot.ballot_id', nullable=False))
    election_id = db.Column(db.Integer, db.ForeignKey('election.election_id'),nullable=False)

class Election(db.Model):
    election_id = db.Column(db.Integer, primary_key=True)
    start_time=db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    end_time=db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    election_status=db.Column(db.String(20), nullable=False) 
    ballot=db.relationship('Ballot', backref='election', lazy=True)  

    


       
