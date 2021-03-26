"""SQLAlchemy models for the dateMeet app"""

from datetime import datetime 

from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """This class holds the structure of the user table for the dateMeet app."""

    __tablename__ = "users"

    id = db.Column(
         db.Integer,
         primary_key=True,
         autoincrement=True
    )

    email = db.Column(
            db.Text,
            nullable=False,
            unique=True
    )

    first_name = db.Column(
                 db.Text,
                 nullable=False,
    )

    last_name = db.Column(
                db.Text,
                nullable=False,
                unique=True
    )

    username = db.Column(
               db.Text,
               nullable=False,
               unique=True
    )

    image_url = db.Column(
                db.Text,
                nullable=True,
                default="/static/images/blank-profile-picture"
    )

    bio = db.Column(
          db.String(250),
          nullable=True
    )

    password = db.Column(
               db.String(30),
               nullable=False
    )

    created_on = db.Column(
                 db.DateTime, 
                 nullable=False, 
                 default=datetime.datetime.now
    )


    locations = db.relationship('Location', backref='users')

    posts  = db.relationship('Post', backref='users')

    likes = db.relationship(
            "Post",
            secondary="likes"
    )

    history = db.relationship('History', backref='users')

  

    def __repr__(self):
        """This method returns a clearer representation of the current user instance."""

        p = self

        return f"<full_name= {p.full_name} username= {p.username} email= {p.email} 
                 created_on= {p.created_on}>"

    def full_name(self):
        """This method formats the first and last anme to form a full name"""
        p = self

        return f"{p.first_name} {p.last_name}"

    @classmethod
    def register(cls, first_name, last_name, email, username, password, image_url):
        """This class method is used to register a new user
           
           It hashes the entered user password and adds the new user to the system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=hashed_pwd,
                image_url=image_url
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """ This class method searches the db with the `username` and `password`
            entered and tries to match this information with an existing user having 
            the same username and whose password hash matches this password.

            If this user is found in the db,  this method returns the user
            if not, it returns False.
        """

        user = cls.query.filter_by(username=username).first()


        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)

            if is_auth:
                return user

        return False 


class Location(db.Model):
    """This class holds the structure of the locations table in the dateMeet db."""

    __tablename__ = "locations"

    id = db.Column(
         db.Integer,
         primary_key=True,
         autoincrement=True
    )

    name = db.Column(
           db.Text,
           nullable=True
    )

    address = db.Column(
              db.Text,
              nullable=False,
              unique=True
    )

    long = db.Column(
           db.Float,
           nullable=False
    )

    lat = db.Column(
          db.Float,
          nullable=False
    )

    user_id = db.Column(
              db.Integer,
              db.ForeignKey('users.id', ondelete='CASCADE'),
              nullable=False
    )

    def __repr__(self):
        """This method returns a clearer representation of the current location instance."""

        p = self

        return f"<address = {p.address} longitude = {p.long} latitude = {p.lat}>"

    
class Post(db.Model):
    """This class holds the structure of the posts table in the dateMeet db."""

    __tablename__ = "posts"

    id = db.Column(
         db.Integer,
         primary_key=True,
         autoincrement=True
    )

    title = db.Column(
            db.String(250),
            nullable=False,

    )

    content = db.Column(
              db.String(500),
              nullable=False
    )

    image_url_1 = db.Column(
                  db.Text,
                  nullable=True
    )

    image_url_2 = db.Column(
                  db.Text,
                  nullable=True
    )

    image_url_3 = db.Column(
                  db.Text,
                  nullable=True
    )

    image_url_4 = db.Column(
                  db.Text,
                  nullable=True
    )

    created_on = db.Column(
                 db.DateTime, 
                 nullable=False, 
                 default=datetime.datetime.now
    )

    user_id = db.Column(
              db.Integer,
              db.ForeignKey('users.id', ondelete='CASCADE'),
              nullable=False
    )


    def __repr__(self):
        """This method returns a clearer representation of the current post instance."""

        p = self

        return f"<title = {p.title} created_on = {p.created_on}>"

class Likes(db.Model):
    """This class holds the structure of the likes table in the dateMeet db."""

    __tablename__ = "likes"

    id = db.Column(
         db.Integer,
         primary_key=True,
         autoincrement=True
    )

    user_id = db.Column(
              db.Integer,
              db.ForeignKey('users.id', ondelete='CASCADE'),
              nullable=False
    )

    post_id = db.Column(
              db.Integer,
              db.ForeignKey('posts.id', ondelete='CASCADE')
    )

    def __repr__(self):
        """This method returns a clearer representation of the current post instance."""

        p = self

        return f"<user_id = {p.user_id} post_id={p.post_id}>"


class History(db.Model):
    """This class holds the structure of the history table in the dateMeet db."""

    __tablename__ = "history"

    id = db.Column(
         db.Integer,
         primary_key=True,
         autoincrement=True
    )

    business_name = db.Column(
                    db.Text
                    nullable=False
    )

    business_address = db.Column(
                       db.Text,
                       nullable=False
    )

    yelp_business_id = db.Column(
                       db.Text,
                       nullable=False
    )

    user_id = db.Column(
              db.Integer,
              db.ForeignKey('users.id', ondelete='CASCADE'),
              nullable=False
    )



    def __repr__(self):
        """This method returns a clearer representation of the current post instance."""

        p = self

        return f"<business_name = {p.business_name} business_address = {p.business_address}>"









