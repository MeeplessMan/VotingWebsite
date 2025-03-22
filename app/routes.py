from flask import Flask, request, Blueprint, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from app import app, db, login, mail, serializer
from app.models import User
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required, AnonymousUserMixin
from flask_mail import Message
from functools import wraps

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
    return redirect(url_for('adminLogin'))

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
    return render_template('admin/index.html', title='Admin Home')

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