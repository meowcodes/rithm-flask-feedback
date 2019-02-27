from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """ Connects to database """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User Model """

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True)
    password = db.Column(db.Text, 
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)

    feedbacks = db.relationship('Feedback',
                           backref='user',
                           cascade="all, delete-orphan")

    @classmethod
    def check_uniqueness(cls, key, value):
        """ Check uniqueness of value """

        pair = {key : value}

        # falsey if unique
        duplicate = User.query.filter_by(**pair).first()

        # return False if duplicate exists
        # return True if no duplicates
        return False if duplicate else True


    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

class Feedback(db.Model):
    """ Feedback Model """

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    title = db.Column(db.String(100), 
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.String(20),
                         db.ForeignKey('users.username'),
                         nullable=False)
