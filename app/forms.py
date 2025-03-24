from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, FileField, RadioField, DateTimeField
from wtforms.validators import DataRequired, InputRequired

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PasswordResetRequestForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')

class UpdateUserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    campus = RadioField(
        'Campus',
        choices=[
            ('Durban', 'Durban'),
            ('Midlands', 'Midlands'),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Update User')

class AddUserForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    fullname = StringField('Full Name', validators=[DataRequired()])
    campus = RadioField(
        'Campus',
        choices=[
            ('Durban', 'Durban'),
            ('Midlands', 'Midlands'),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Add User')

class AddUsersForm(FlaskForm):
    file = FileField('Upload Text File', validators=[InputRequired()])
    submit = SubmitField('Add Users')

class AddCandidateForm(FlaskForm):
    image = FileField('Candidate Image', validators=[DataRequired()])
    candidate_name = StringField('Candidate Name', validators=[DataRequired()])
    manifesto = StringField('Manifesto', validators=[DataRequired()])
    campus = StringField('Campus', validators=[DataRequired()])
    submit = SubmitField('Add Candidate')

class ElectionForm(FlaskForm):
    election_name = StringField('Election Name', validators=[DataRequired()])
    election_name = StringField('Election Name', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %I:%M %p', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %I:%M %p', validators=[DataRequired()])
    submit = SubmitField('Create Election')

class UpdateElectionForm(FlaskForm):
    election_name = StringField('Election Name', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %I:%M %p', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %I:%M %p', validators=[DataRequired()])
    submit = SubmitField('Update Election')