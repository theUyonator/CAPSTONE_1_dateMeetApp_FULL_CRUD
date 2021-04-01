"""This app file contains all view functions for the dateMeet app"""

import os 

from flask import Flask, render_template, request, flash, redirect, session, g, abort 
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError 

from forms import UserRegisterForm, UserEditForm, UserLoginForm, UserLocationForm
from models import db, connect_db, User, Post

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
Bootstrap(app)

# For production and testing we need to get the DB_URI from environ variable 
# If not DB_URI not yet set in environ variable, we use the development local db.

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///dateMeet'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "dateMeetisgr8")
toolbar = DebugToolbarExtension(app)

connect_db(app)

####################################################################################################
# User register/login/logout 

@app.before_request
def add_user_to_g():
    """If a user is logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def login_user(user):
    """This function logs in an existing user"""

    session[CURR_USER_KEY] = user.id

def logout_user():
    """This function logs out a current user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/register', methods=["GET", "POST"])
def register():
    """This view function handles the registeration of a new user.

       It creates a new user and adds to the dateMeet DB, then redirects to the home page.

       If form is not valid, present form.

       If there is already an existing user with the entered username: flash message 
       and represent form.
    """

    logout_user()

    form = UserRegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                username = form.username.data,
                email = form.email.data,
                password = form.password.data,
                image_url = form.image_url.data
            )

            db.session.commit()

        except IntegrityError:
            flash("Username already exist", 'danger')
            return render_template('users/register.html', form=form)

        login_user(user)

        return redirect("/")

    else: 
        return render_template('users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """This view function handles the login of an existing user"""

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
                                  form.username.data,
                                  form.password.data)
                            
                    
        if user:
            login_user(user)
            flash(f"Welcome, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """This view function handles the logout of an existing user."""

    logout_user()

    flash("You have succesfully logged out of the dateMeet app.", 'success')
    return redirect("/login")


####################################################################################
#General user routes:




##################################################################################
# Homepage and error pages

@app.route('/')
def homepage():
    """This view function takes you to the dateMeet homepage
    
    - anon users: no messages
    -logged in: 50 most recent posts by users if a city has not been entered. 
    
    """

    if g.user:
        form=UserLocationForm()
        return render_template('home.html',form=form)

    else:
        return render_template('home-anon.html')


