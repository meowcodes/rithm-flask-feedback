from flask import Flask, request, render_template, redirect, jsonify, session
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
        username = form.username.data
        password = form.password.data
        
        user = User.register(username, password)

        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        return redirect ('/secret')
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods = ['GET', 'POST']) 
def log_in():
    """" render login page and handle login process"""
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authentiate(username, password)

        if user:
            session["username"] = user.username
            return redirect("/secret")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login.html", form=form)


@app.route('/secret') 
def secret():

    if "username" in session:
        return "You made it!"
    else:
        return redirect('/')