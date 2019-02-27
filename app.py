from flask import Flask, request, render_template, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app= Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)

@app.route('/') 
def show_index():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST']) 
def registeration():
    """" render register page and handle register process"""
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        username_unique = User.check_uniqueness("username", username)
        email_unique = User.check_uniqueness("email", email)

        if username_unique and email_unique:
            user = User.register(username, password)

            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data

            db.session.add(user)
            db.session.commit()

            session["username"] = user.username

            return redirect(f"/users/{username}")

        elif not username_unique:
            form.username.errors = ["Username already exists."]

        elif not email_unique:
            form.email.errors = ["Email already exists."]
    
    return render_template("register.html", form=form)


@app.route('/login', methods = ['GET', 'POST']) 
def log_in():
    """" render login page and handle login process"""
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Bad username/password"]

    return render_template("login.html", form=form)


@app.route('/logout') 
def logout():    
    """ loging out users by removing they username form session """
    session.pop("username")
    return redirect('/')

@app.route('/users/<username>') 
def user_details(username):
    """" show user_details page to the same user who has logged in"""
    if session["username"] == username:
        # if user is authorized, render user_details
        user = User.query.filter_by(username=username).first()

        return render_template('user_details.html', user = user)
    else:
        flash('You need to register and log in to view this page')
        return redirect('/')


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """ Remove user from database """

    if session["username"] == username:

        user = User.query.filter_by(username=username).first()

        db.session.delete(user)
        db.session.commit()

        session.pop("username")

        return redirect("/")
    else:
        flash('You need to register and log in to view this page')
        return redirect('/')


@app.route('/users/<username>/feedback/add', methods=["GET","POST"])
def add_feedback(username):
    """ Show and process add feedback form """

    form = FeedbackForm()
    
    if session["username"] == username:

        user = User.query.filter_by(username=username).first()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            
            new_feedback=Feedback(title=title, content=content, username=username)
            
            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f"/users/{user.username}")
        else:
            return render_template("add_feedback.html", form=form, user=user)
    else:
        flash('You need to register and log in to view this page')
        return redirect('/')


@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """ Show and process edit feedback form """
    
    feedback = Feedback.query.get(feedback_id)
    
    form = FeedbackForm(title=feedback.title, content=feedback.content)
    
    if session["username"] == feedback.user.username:
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            
            db.session.commit()

            return redirect(f"/users/{feedback.user.username}")
        else:
            return render_template("update_feedback.html", form=form, feedback=feedback)
    else:
        flash('You need to register and log in to view this page')
        return redirect('/')


@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """ Delete feedback """
    feedback = Feedback.query.get(feedback_id)
    
    if session["username"] == feedback.user.username:

        db.session.delete(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.user.username}")
    else:
        flash('You need to register and log in to view this page')
        return redirect('/')
