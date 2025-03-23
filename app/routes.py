from flask import Flask, request, Blueprint, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from app import app, db, login, mail, serializer
from app.models import User, Ballot, Vote, Candidate, Election
from app.forms import LoginForm, UpdateUserForm, AddCandidateForm, AddUserForm, AddUsersForm, UpdateUserForm
from app.methods import Methods
from flask_login import current_user, login_user, logout_user, login_required, AnonymousUserMixin
from flask_mail import Message
from functools import wraps
from werkzeug.utils import secure_filename
import os

def generate_verification_token(email):
    return serializer.dumps(email, salt='shadow-Wizard-money-gang')

def verify_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt='shadow-Wizard-money-gang', max_age=expiration)
    except:
        return False
    return email

def role_required(role="admin"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            print(f'Checking if user has the required permissions to access this page.')
            if not current_user or isinstance(current_user, AnonymousUserMixin):
                flash('You must be logged in to access this page.')
                return redirect(url_for('voterLogin'))
            urole = current_user.role
            if ( (urole != role) and (role != "ANY")):
                logout_user()
                flash('You do not have the required permissions to access this page.')
                return redirect(url_for('voterLogin'))     
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Admin routes

@app.route('/')
@login_required
def index():
    return redirect(url_for('voterLogin'))

@app.route('/admin/login', methods=['POST', 'GET'])
def adminLogin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            token = generate_verification_token(user.email)
            verify_url = url_for('adminVerify', token=token, _external=True)
            html = render_template('admin/activate.html', verify_url=verify_url, title='Verify Email')
            subject = 'Please verify your email'
            msg = Message(subject, recipients=[user.email], html=html)
            mail.send(msg)
            flash('A verification email has been sent to your email.')
            return redirect(url_for('adminLogin'))
        flash('Invalid email or password.')
        return redirect(url_for('adminLogin'))
    return render_template('admin/login.html', title='Sign in', form=form)

@app.route('/admin/verify/<token>')
def adminVerify(token):
    email = verify_token(token)
    if email:
        user = User.query.filter_by(email=email).first()
        login_user(user, remember=True)
        flash('Email verified successfully.')
        return redirect(url_for('adminIndex'))
    flash('The verification link is invalid or has expired.')
    return redirect(url_for('adminLogin'))


@app.route('/admin/logout')
@role_required(role="admin")
@login_required
def adminLogout():
    logout_user()
    return redirect(url_for('adminLogin'))


@app.route('/admin/index')
@app.route('/admin/')
@role_required(role="admin")
@login_required
def adminIndex():
    return render_template('admin/index.html', title='Admin Dashboard')

@app.route('/admin/profile')
@role_required(role="admin")
@login_required
def adminProfile():
    return render_template('admin/Profile/profile.html', title='Admin Profile')

@app.route('/admin/users')
@role_required(role="admin")
@login_required
def adminUsers():
    users = User.query.all()
    return render_template('admin/Users/users.html', title='Users', users=users)

@app.route('/admin/users/update/<int:id>', methods=['GET', 'POST'])
@role_required(role="admin")
@login_required
def adminUserUpdate(id):
    user = User.query.get(id)
    if(user == None):
        flash('User not found.')
        return redirect(url_for('adminUsers'))
    form = UpdateUserForm()
    if form.validate_on_submit():
        user.email = form.email.data
        if(Methods.check_dut_email(user.email) == False):
            flash('Only DUT emails are allowed.')
            return redirect(url_for('adminUserUpdate', id=user.id))
        user.fullname = form.fullname.data
        user.campus = form.campus.data
        db.session.commit()
        flash(f'{user.fullname} updated successfully.')
        return redirect(url_for('adminUsers'))
    elif request.method == 'GET':
        form.email.data = user.email
        form.fullname.data = user.fullname
        form.campus.data = user.campus
    return render_template('admin/Users/UpdateUser.html', title='Update User', form=form, user=user)

@app.route('/admin/users/add', methods=['GET', 'POST'])
@role_required(role="admin")
@login_required
def adminUserAdd():
    form = AddUserForm()
    form2 = AddUsersForm()
    if form.validate_on_submit():
        email = form.email.data
        fullname = form.fullname.data
        campus = form.campus.data
        if(Methods.check_dut_email(email) == False):
            flash('Only DUT emails are allowed.')
            return redirect(url_for('adminUserAdd'))
        if(User.query.filter_by(email=email).first()):
            flash('User already exists.')
            return redirect(url_for('adminUserAdd'))
        user = User(email=email, fullname=fullname, campus=campus)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        flash(f'{user.fullname} added successfully.')
        return redirect(url_for('adminUsers'))
    elif form2.validate_on_submit():
        file = form2.file.data
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('adminUserAdd'))
        if file:
            f = secure_filename(file.filename)
            file.save(f)
            with open(f, 'r') as f:
                for line in f:
                    print(line)
                    try:
                        email, fullname, campus = line.split('#')
                    except:
                        os.remove(file.filename)
                        flash('Invalid data. Reconfigure your text file: Format: email#fullname#campus')
                        return redirect(url_for('adminUserAdd'))
                    if(Methods.check_dut_email(email) == False):
                        os.remove(file.filename)
                        flash('Only DUT emails are allowed.')
                        return redirect(url_for('adminUserAdd'))
                    if(fullname == '' or campus == ''):
                        os.remove(file.filename)
                        flash('Invalid data. Reconfigure your text file: Format: email#fullname#campus')
                        return redirect(url_for('adminUserAdd'))
                    user = User.query.filter_by(email=email).first()
                    if(user != None):
                        user.registered = True
                        user.fullname = fullname
                        user.campus = campus
                        db.session.commit()
                        continue
                    user = User(email=email, fullname=fullname, campus=campus)
                    user.set_password('DUT4Life'+email.split('@')[0])
                    db.session.add(user)
                    db.session.commit()
            os.remove(file.filename)
            flash('Users added successfully.')
            return redirect(url_for('adminUsers'))
        if request.method == 'GET':
            form.email.data = user.email
            form.fullname.data = user.fullname
            form.campus.data = user.campus
    return render_template('admin/Users/AddUsers.html', title='Add User', form=form, form2=form2)

@app.route('/admin/users/delete/<int:id>')
@role_required(role="admin")
@login_required
def adminUserDelete(id):
    user = User.query.get(id)
    if(user == None):
        flash('User not found.')
        return redirect(url_for('adminUsers'))
    if user == current_user:
        flash('You cannot delete yourself.')
        return redirect(url_for('adminUsers'))
    if user.has_role('admin'):
        flash('You cannot delete an admin user.')
        return redirect(url_for('adminUsers'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('adminUsers'))

@app.route('/admin/candidates')
@role_required(role="admin")
@login_required
def adminCandidates():
    candidates = Candidate.query.all()
    return render_template('admin/Candidates/candidates.html', title='Candidates', candidates=candidates)

@app.route('/admin/elections')
@role_required(role="admin")
@login_required
def adminElections():
    elections = Election.query.all()
    return render_template('admin/Elections/elections.html', title='Elections', elections=elections)

# Voter routes

@app.route('/voter/index')
@app.route('/voter/')
@login_required
def voterIndex():
    return render_template('voter/index.html', title='Voter Home')

@app.route('/voter/login', methods=['GET','POST'])
def voterLogin():
    if current_user.is_authenticated:
        return redirect(url_for('voterIndex'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            token = generate_verification_token(user.email)
            verify_url = url_for('voterVerify', token=token, _external=True)
            html = render_template('voter/activate.html', verify_url=verify_url, title='Verify Email')
            subject = 'Please verify your email'
            msg = Message(subject, recipients=[user.email], html=html)
            mail.send(msg)
            flash('A verification email has been sent to your email.')
            return redirect(url_for('voterLogin'))
        flash('Invalid email or password.')
        return redirect(url_for('voterLogin'))
    return render_template('voter/login.html', title="Voter Sign In", form=form)

@app.route('/voter/verify/<token>')
def voterVerify(token):
    email = verify_token(token)
    if email:
        user = User.query.filter_by(email=email).first()
        print(user)
        login_user(user, remember=True)
        flash('Email verified successfully.')
        return redirect(url_for('voterIndex'))
    flash('The verification link is invalid or has expired.')
    return redirect(url_for('voterLogin'))

@app.route('/voter/about')
@login_required
def voterAbout():
    return render_template('voter/about.html', title='About')

@app.route('/voter/logout')
@login_required
def voterLogout():
    logout_user()
    return redirect(url_for('voterLogin'))

@app.route('/voter/instructions')
@login_required
def voterInstructions():
    return render_template('voter/instructions.html', title='Voter Instructions')