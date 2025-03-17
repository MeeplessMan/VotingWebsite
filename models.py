from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Student(db.Model):
    Student_id = db.Column(db.Integer, primary_key=True)
    FullName = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Campus = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(100), nullable=False)
    HasVoted = db.Column(db.String(100), nullable=False)
    Date_created = db.Column(db.DateTime, default=datetime.utcnow)
    Ballots = db.relationship('Ballot', backref='student', lazy=True)
    Confirmation_Emails = db.relationship('Confirmation_Email', backref='student', lazy=True)
    
    #def set_password(self, password):
        #hash the password before saving
      #  self.Password = generate_password_hash(password)

    #def check_password(self, password):
        #check if hashed password matches actual password
       # return check_password_hash(self.Password, password)
    
class Ballot(db.Model):
    Ballot_id = db.Column(db.Integer, primary_key=True)
    Candidate_List= db.Column(db.String(100), nullable=False)
    Campus= db.Column(db.String(100), nullable=False)
    Max_Selection= db.Column(db.Integer, nullable=False)
    Status= db.Column(db.String(100), nullable=False)
    Voting_Options= db.Column(db.String(100), nullable=False)
    Date_created = db.Column(db.DateTime, default=datetime.utcnow)
    Election_id = db.Column(db.Integer, db.ForeignKey('election.Election_id'), nullable=False)
    Student_id= db.Column(db.Integer, db.ForeignKey('student.Student_id'), nullable=False)
    Votes = db.relationship('Vote', backref='ballot', lazy=True)

class Vote(db.Model):
    Vote_id = db.Column(db.Integer, primary_key=True)
    Encrypted_Vote_Data = db.Column(db.String(100), nullable=False)
    Date_created = db.Column(db.DateTime, default=datetime.utcnow)
    TimeStamp = db.Column(db.DateTime, default=datetime.utcnow)
    Student= db.relationship('Student', backref='vote', lazy=True)
    Ballot_id = db.Column(db.Integer, db.ForeignKey('ballot.Ballot_id'), nullable=False)
    Candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.Candidate_Id'), nullable=False)

class Confirmation_Email(db.Model):
    Email_id = db.Column(db.Integer, primary_key=True)
    TimeStamp = db.Column(db.DateTime, default=datetime.utcnow)
    Date_created = db.Column(db.DateTime, default=datetime.utcnow)
    Status = db.Column(db.String(100), nullable=False)
    Student_id=db.relationship('Student', backref='confirmation_email', lazy=True)

class Candidate(db.Model):
    Candidate_Id=db.Column(db.Integer, primary_key=True)
    Candidate_Name=db.Column(db.String(100), nullable=False)
    Manifesto=db.Column(db.String(100), nullable=False)
    Campus=db.Column(db.String(100), nullable=False)
    Total_Votes=db.Column(db.Integer, nullable=False)
    Date_created = db.Column(db.DateTime, default=datetime.utcnow)
    Votes=db.relationship('Vote', backref='candidate', lazy=True)
    Election_id = db.Column(db.Integer, db.ForeignKey('election.Election_id'), nullable=False)

class Election(db.Model):
    Election_id = db.Column(db.Integer, primary_key=True)
    Start_Time=db.Column(db.DateTime, default=datetime.utcnow)
    End_Time=db.Column(db.DateTime, default=datetime.utcnow)
    Election_Status=db.Column(db.String(100), nullable=False)  
    Candidates=db.relationship('Candidate', backref='election', lazy=True)  

    


       
