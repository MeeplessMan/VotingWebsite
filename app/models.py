from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import RoleMixin
from datetime import datetime
from app.routes import login
from flask_login import UserMixin
from app import db, login

roles_users = db.table(roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))))

class User(UserMixin,db.Model):
    user_id = db.Column(db.String(10), primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nulllable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.relationship('Role', secondary = roles_users, backref=db.backref('users', lazy='dynamic'))
   
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.user_id)
    
    def has_role(self, role_name):
        """Does this user have this permission?"""
        my_role = Role.query.filter_by(name=role_name).first()
        if my_role in self.roles:
            return True
        else:
            return False
    
    
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Election(db.Model):
    election_id = db.Column(db.Integer, primary_key=True)
    election_name = db.Column(db.String(80), nullable = False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    election_status =db.Column(db.Boolean, default=False)
    users = db.relationship('User',  backref=db.backref('elections', lazy= True))

class Candidate(db.Model):
    candidate_id = db.Column(db.Integer, primary_key=True)
    voting_options = db.Column(db.Boolean, default=False)
    elections = db.relationship('Elections', backref=db.backref('candidate', lazy=True))

class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,default=datetime)
    #encrypted_vote_data = 
    users = db.relationship('users', backref=db.backref('vote', lazy=True))
    elections = db.relationship('elections', backref=db.backref('vote', lazy=True))
    candidates = db.relationship('candidates',  backref=db.backref('vote', lazy= True))

