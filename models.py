from flask_sqlalchemy import SQLAlchemy
db= SQLAlchemy()

def connect_db(app):
    """ Connects to database """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User Model """

    username = db.Column(db.String(20),
                         primary_key=True)
    password = db.Column(db.Text, 
                         nullable=False)
    email = db,Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)


    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)