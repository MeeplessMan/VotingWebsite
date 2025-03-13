from flask import Flask, redirect, request, flash, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('signup.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/vote')
def voting():
    return render_template('StudentVotingUI.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

if __name__ == '__main__':
    app.run(debug=True)