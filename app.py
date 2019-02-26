from flask import Flask, request, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm


app= Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)


@app.route('/') 
def show_index():
    return redirect('/register')


@app.route('/register', methods = ['GET', 'POST']) 
def registeration():
    """" render register page and handle register process"""
    
    form = RegisterForm()

    if form.validate_on_submit():
        #  call the classmethod register on User class
        return redirect ('/secret')

    else:
        return render_template("register.html", form=form)


@app.route('/login', methods = ['GET', 'POST']) 
def log_in():
    """" render login page and handle login process"""
    
    form = LoginForm()

    if form.validate_on_submit():
        #  call the classmethod login on User class
        return redirect ('/secret')

    else:
        return render_template("login.html", form=form)

