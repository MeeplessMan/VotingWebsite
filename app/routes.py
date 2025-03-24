from flask import Flask, request, Blueprint, redirect, url_for, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from app import app, db, login, mail, serializer
from app.models import User, Ballot, Vote, Candidate, Election
from app.forms import LoginForm, UpdateBallotForm, UpdateCandidateForm, UpdateUserForm, AddCandidateForm, AddUserForm, AddUsersForm, UpdateUserForm, PasswordResetForm, PasswordResetRequestForm, ElectionForm, UpdateElectionForm, SetElectinoStatusForm
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
            file = file.read().decode('utf-8').splitlines()
            print(file)
            for line in file:
                    print(line)
                    try:
                        email, fullname, campus = line.split('#')
                    except:
                        flash('Invalid data. Reconfigure your text file: Format: email#fullname#campus1')
                        return redirect(url_for('adminUserAdd'))
                    if email == '' or fullname == '' or campus != 'Durban' and campus != 'Midlands':
                        flash('Invalid data. Reconfigure your text file: Format: email#fullname#campus2')
                        return redirect(url_for('adminUserAdd'))
                    if(Methods.check_dut_email(email) == False):
                        flash('Only DUT emails are allowed.')
                        return redirect(url_for('adminUserAdd'))
                    if(fullname == '' or campus == ''):
                        flash('Invalid data. Reconfigure your text file: Format: email#fullname#campus3')
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

@app.route('/admin/candidates/profile/<int:id>')
@role_required(role="admin")
@login_required
def adminCandidateProfile(id):
    candidate = Candidate.query.get(id)
    if candidate is None:
        flash('Candidate not found.')
        return redirect(url_for('adminCandidates'))
    return render_template('admin/Candidates/profile.html', title='Candidate Profile', candidate=candidate)

@app.route('/admin/candidates/add/<int:id>', methods=['GET', 'POST'])
@role_required(role="admin")
@login_required
def adminCandidateAdd(id):
    form = AddCandidateForm()
    if form.validate_on_submit():
        image = form.image.data
        candidate_name = form.candidate_name.data
        manifesto = form.manifesto.data
        ballot_id = id
        if Methods.check_image(image.filename) == False:
            flash('Invalid image format: require .png.')
            return redirect(url_for('adminCandidateAdd'))
        test = Methods.create_candidate(candidate_name, manifesto, ballot_id)
        if test:
            candidate = Candidate.query.filter_by(fullname=candidate_name).first()
            if image.filename != '':
                filename = secure_filename(str(candidate.id) + '.jpg')
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'{candidate_name} added successfully.')
        else:
            flash('An error occurred.')
        return redirect(url_for('adminCandidates'))
    if request.method == 'GET':
        form.candidate_name.data = form.candidate_name.data
        form.manifesto.data = form.manifesto.data
    return render_template('admin/Candidates/addCandidate.html', title='Add Candidate', form=form, id=id)

@app.route('/admin/candidates/update/<int:id>', methods=['GET', 'POST'])
@role_required(role="admin")
@login_required
def adminCandidateUpdate(id):
    candidate = Candidate.query.get(id)
    form = UpdateCandidateForm()
    if candidate is None:
        flash('Candidate not found.')
        return redirect(url_for('adminCandidates'))
    if form.validate_on_submit():
        fullname = form.fullname.data
        manifesto = form.manifesto.data
        campus = form.campus.data
        image = form.image.data
        if image.filename == '':
            flash('No selected file')
            return redirect(url_for('adminCandidateUpdate', id=candidate.id))
        if candidate.fullname != fullname:
            candidate.fullname = fullname
        if candidate.manifesto != manifesto:
            candidate.manifesto = manifesto
        if candidate.campus != campus:
            if candidate.campus != 'Durban' and candidate.campus != 'Midlands':
                candidate.campus = campus    
            elif campus == 'Durban':
                candidate.ballot_id = candidate.ballot_id - 1
            else:
                candidate.ballot_id = candidate.ballot_id + 1
            candidate.campus = campus
        db.session.commit()
        if Methods.check_image(image.filename) == False:
            flash('Invalid image format: require .jpg')
            return redirect(url_for('adminCandidateUpdate', id=candidate.id))
        filename = secure_filename(str(candidate.id) + '.jpg')
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except:
            pass
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'{candidate.fullname} updated successfully.')
        return redirect(url_for('adminCandidates'))
    elif request.method == 'GET':
        form.fullname.data = candidate.fullname
        form.manifesto.data = candidate.manifesto
    return render_template('admin/Candidates/updateCandidate.html', title='Update Candidate', id=candidate.id, form=form)

@app.route('/admin/candidates/delete/<int:id>')
@role_required(role="admin")
@login_required
def adminCandidateDelete(id):
    candidate = Candidate.query.get(id)
    if candidate is None:
        flash('Candidate not found.')
        return redirect(url_for('adminCandidates'))
    test = Methods.delete_candidate(candidate.id)
    if test:
        flash('Candidate deleted successfully.')
        return redirect(url_for('adminCandidates'))
    flash('An error occurred.')
    return redirect(url_for('adminCandidates'))


@app.route('/admin/elections')
@role_required(role="admin")
@login_required
def adminElections():
    elections = Election.query.all()
    return render_template('admin/Elections/elections.html', title='Elections', elections=elections)

@app.route('/admin/current_election', methods=['GET'])
@role_required(role="admin")
@login_required
def adminCurrentElection():
    election = Methods.get_current_election()
    if election is None:
        flash('No current election. Showing upcoming election.')
        election = Methods.get_upcoming_election()
        if election is None:
            flash('No upcoming election. Showing Elections.')
            return redirect(url_for('adminElections'))
    return render_template('admin/Elections/currentElection.html', title='Current Election', election=election)

@app.route('/admin/ballots')
@role_required(role="admin")
@login_required
def adminBallots():
    ballots = Ballot.query.all()
    return render_template('admin/Ballots/ballots.html', title='Ballots', ballots=ballots)

@app.route('/admin/elections/add', methods=['GET', 'POST'])
@login_required
@role_required(role="admin")
def adminElectionAdd():
    form = ElectionForm()
    if form.validate_on_submit():
        election_name = form.election_name.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        election = Election.query.filter_by(election_name=election_name).first()
        if election is not None:
            flash('Election already exists.')
            return redirect(url_for('adminElectionAdd'))
        success = Methods.create_election(election_name, start_time, end_time)
        if success:
            election = Election.query.filter_by(election_name=election_name).first()
            Methods.create_ballot('Durban', 8, election.id)
            Methods.create_ballot('Midlands', 7, election.id)
            flash(f'{election_name} added successfully with corresponding ballots.')
            return redirect(url_for('adminElections'))
        flash('An error occurred')
        return redirect(url_for('adminElectionAdd'))
    return render_template('admin/Elections/createElection.html', title='Add Election', form=form)

@app.route('/admin/election/delete/<int:id>')
@login_required
@role_required(role="admin")
def adminElectionDelete(id):
    election = Election.query.get(id)
    if election is None:
        flash('Election not found.')
        return redirect(url_for('adminElections'))
    db.session.delete(election)
    db.session.commit()
    flash('Election deleted successfully.')
    return redirect(url_for('adminElections'))

@app.route('/admin/election/update/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(role="admin")
def adminElectionUpdate(id):
    form = UpdateElectionForm()
    form2 = SetElectinoStatusForm()
    election = Election.query.get(id)
    if election is None:
        flash('Election not found.')
        return redirect(url_for('adminElections'))
    if form.validate_on_submit():
        election.election_name = form.election_name.data
        election.start_time = form.start_time.data
        election.end_time = form.end_time.data
        test = Methods.update_election(election.id, election.election_name, election.start_time, election.end_time)
        if test:
            flash(f'{election.election_name} updated successfully.')
            return redirect(url_for('adminElections'))
        flash('An error occurred.')
        return redirect(url_for('adminElectionUpdate', id=election.id))
    elif form2.validate_on_submit():
        status = form2.status.data
        test = Methods.set_election_status(election.id, status)
        if test:
            flash(f'{election.election_name} status updated successfully.')
            return redirect(url_for('adminElections'))
        flash('An error occurred.')
        return redirect(url_for('adminElectionUpdate', id=election.id))
    elif request.method == 'GET':
        form.election_name.data = election.election_name
        form.start_time.data = election.start_time
        form.end_time.data = election.end_time
        form2.status.data = election.election_status
    return render_template('admin/Elections/updateElection.html', title='Update Election', form=form, election=election, form2=form2)

@app.route('/admin/reset_password', methods=['GET'])
@role_required(role="admin")
@login_required
def adminResetPassword():
    token = generate_verification_token(current_user.email)
    verify_url = url_for('adminPasswordReset', token=token, _external=True)
    html = render_template('admin/Profile/resetEmail.html', verify_url=verify_url, title='Password Reset')
    subject = 'Password Reset'
    msg = Message(subject, recipients=[current_user.email], html=html)
    mail.send(msg)
    flash('A password reset has been sent to your email.')
    return redirect(url_for('adminIndex'))

@app.route('/admin/reset_password/<token>', methods=['GET', 'POST'])
@role_required(role="admin")
@login_required
def adminPasswordReset(token):
    email = verify_token(token)
    if email:
        user = User.query.filter_by(email=email).first()
        form = PasswordResetForm()
        if form.validate_on_submit():
            password = form.password.data
            if password == '':
                flash('Password cannot be empty.')
                return redirect(url_for('adminPasswordReset', token=token))
            if user.check_password(password):
                flash('Password cannot be the same as the previous one.')
                return redirect(url_for('adminPasswordReset', token=token))
            user.set_password(password)
            db.session.commit()
            flash('Password reset successfully.')
            return redirect(url_for('adminIndex'))
        return render_template('admin/Profile/resetPassword.html', title='Reset Password', form=form, token=token)
    flash('The verification link is invalid or has expired.')
    return redirect(url_for('adminIndex'))
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