"""SQLAlchemy models for the dateMeet app"""

import datetime 

from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Follows(db.Model):
    """This class holds the structure of the follows table for the dateMeet app.
    It is the connection btw a follower <--> followed_user
    """

    __tablename__ = "follows"
    
    id = db.Column(
         db.Integer,
         primary_key=True,
         autoincrement=True
    )

    user_being_followed_id = db.Column(
                             db.Integer,
                             db.ForeignKey('users.id', ondelete="cascade"),
                             primary_key=True,
    )

    user_following_id = db.Column(
                        db.Integer,
                        db.ForeignKey('users.id', ondelete="cascade"),
                        primary_key=True,
    )

# Note that the follows table has two foreign keys to the same table user, 
# This is because each of these foreigns keys track data in two scenarios
# While user_being_followed holds data of the other users a current user is following,
# user_following holds information on the other users following the current / logged in user.


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
    )

    username = db.Column(
               db.Text,
               nullable=False,
               unique=True
    )

    image_url = db.Column(
                db.Text,
                nullable=True,
                default="/static/blank-profile-picture.png"
    )

    header_url = db.Column(
                db.Text,
                nullable=True,
                default="/static/blank-header-picture.jpeg"
    )

    bio = db.Column(
          db.String(250),
          nullable=True
    )

    password = db.Column(
               db.Text,
               nullable=False
    )

    created_on = db.Column(
                 db.DateTime, 
                 nullable=False, 
                 default=datetime.datetime.now
    )


    locations = db.relationship('Location', backref='users')

    recommendations  = db.relationship('Recommendation', backref='user')

    followers = db.relationship(
                "User",
                secondary="follows",
                primaryjoin=(Follows.user_being_followed_id == id),
                secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
                "User",
                secondary="follows",
                primaryjoin=(Follows.user_following_id == id),
                secondaryjoin=(Follows.user_being_followed_id == id)
    )

    likes = db.relationship(
            "Recommendation",
            secondary="likes"
    )

    # history = db.relationship('History', backref='users')


    def __repr__(self):
        """This method returns a clearer representation of the current user instance."""

        p = self

        return f"<full_name= {p.full_name} username= {p.username} email= {p.email} created_on= {p.created_on}>"

    def is_following(self, other_user):
        """This method checks if the signed in user is following `other_user`"""

        user_following_list = [user for user in self.following if user == other_user]
        return len(user_following_list) == 1

    def is_followed_by(self, other_user):
        """This method checks if the signed in user is being followed by `other_user`"""

        user_followed_by_list = [user for user in self.followers if user == other_user]
        return len(user_followed_by_list) == 1

    def full_name(self):
        """This method formats the first and last anme to form a full name"""
        p = self

        return f"{p.first_name} {p.last_name}"

    @classmethod
    def register(cls, first_name, last_name, email, username, password, image_url, header_url):
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
                image_url=image_url,
                header_url=header_url
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
           nullable=False
    )

    address = db.Column(
              db.Text,
              nullable=False
    )

    long = db.Column(
           db.Float,
           nullable=False
    )

    lat = db.Column(
          db.Float,
          nullable=False
    )

    city = db.Column(
                    db.Text,
                    nullable=False
    )

    state = db.Column(
                       db.Text,
                       nullable=False
    )

    entered_on = db.Column(
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
        """This method returns a clearer representation of the current location instance."""

        p = self

        return f"<address = {p.address} longitude = {p.long} latitude = {p.lat}>"

    
class Recommendation(db.Model):
    """This class holds the structure of the posts table in the dateMeet db."""

    __tablename__ = "recommendations"

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

    business_name = db.Column(
                    db.Text,
                    nullable=False
    )
    business_address = db.Column(
                        db.Text,
                        nullable=False
    )
    
    business_city = db.Column(
                    db.Text,
                    nullable=False
    )

    business_state = db.Column(
                     db.Text,
                     nullable=False
    )

    business_country = db.Column(
                       db.Text,
                       nullable=False
    )

    business_rating = db.Column(
                      db.Integer,
                      nullable=False
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

    recommendation_id = db.Column(
              db.Integer,
              db.ForeignKey('recommendations.id', ondelete='CASCADE')
    )

    def __repr__(self):
        """This method returns a clearer representation of the current post instance."""

        p = self

        return f"<user_id = {p.user_id} recommendation_id={p.recommendation_id}>"


def connect_db(app):
    """This method connects this database to provided Flask app

       This method should be called in the Flask app.
       """

    db.app = app
    db.init_app(app)


# class History(db.Model):
#     """This class holds the structure of the history table in the dateMeet db."""

#     __tablename__ = "history"

#     id = db.Column(
#          db.Integer,
#          primary_key=True,
#          autoincrement=True
#     )

#     business_name = db.Column(
#                     db.Text,
#                     nullable=False
#     )

#     business_address = db.Column(
#                        db.Text,
#                        nullable=False
#     )

#     yelp_business_id = db.Column(
#                        db.Text,
#                        nullable=False
#     )

#     yelp_business_url = db.Column(
#                         db.Text,
#                         nullable=True
#     )

#     user_id = db.Column(
#               db.Integer,
#               db.ForeignKey('users.id', ondelete='CASCADE'),
#               nullable=False
#     )



#     def __repr__(self):
#         """This method returns a clearer representation of the current post instance."""

#         p = self

#         return f"<business_name = {p.business_name} business_address = {p.business_address}>"








