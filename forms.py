from flask_wtf import FlaskForm
# from flask_wtf.html5 import URLField
from wtforms import StringField, FloatField, IntegerField, BooleanField, RadioField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    """" Form for Adding User to the user data table"""
    
    username = StringField(" Username: ",
                           validators=[InputRequired(), Length(min=1, max=20)])
    password = StringField(" Password: ",
                           validators=[InputRequired()])
    email = StringField(" Email: ",
                           validators=[InputRequired(), Email(), Length(min=1, max=50)])
    first_name = StringField(" First Name: ",
                           validators=[InputRequired(), Length(min=1, max=30)])
    last_name = StringField(" Last Name: ",
                           validators=[InputRequired(), Length(min=1, max=30)])
    