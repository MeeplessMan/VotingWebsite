from flask import Flask, request, Blueprint, redirect, url_for, request, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from app import app
from app.forms import LoginForm

@app.route('/')
def index():
    return redirect(url_for('voterIndex'))

@app.route('/admin/login', methods=['POST', 'GET'])
@app.route('/admin/')
def adminLogin():
    form = LoginForm()
    return render_template('admin/login.html', title='Sign in', form=form)

@app.route('/voter/index')
@app.route('/voter/')
def voterIndex():
    return render_template('voter/index.html')

@app.route('/voter/logini', methods=['GET','POST'])
def voterLogin():
    form = LoginForm()
    return render_template('voter/login.html', title="Sign In", form=form)

if __name__ == '__main__':
    app.run(debug=True)