from flask import Flask, request, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Deck, Suit

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
def register():
    """" render register page and handle register process"""
    


    return redirect('/register')