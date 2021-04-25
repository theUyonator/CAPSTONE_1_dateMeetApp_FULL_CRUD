"""This app file contains all view functions for the dateMeet app"""

import os 

from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify 
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError 

from forms import UserRegisterForm, UserEditForm, UserLoginForm, UserLocationForm, EditUserLocationForm
from models import db, connect_db, User, Post, Location
from helpers import get_lat_lng, yelp_business_search
from secrets import YELP_API_SECRET_KEY, GEOCODE_API_KEY

CURR_USER_KEY = "curr_user"
CURR_LOCATION = "None"

app = Flask(__name__)
Bootstrap(app)

# For production and testing we need to get the DB_URI from environ variable 
# If not DB_URI not yet set in environ variable, we use the development local db.

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///dateMeet'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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

@app.before_request
def add_user_location():
    """If a is logged in and has entered a location, save that location to Flask global"""

    if g.user:
        if CURR_LOCATION in session:
            g.location = Location.query.get(session[CURR_LOCATION])
        else:
            g.location = None

def login_user(user):
    """This function logs in an existing user"""

    session[CURR_USER_KEY] = user.id

def logout_user():
    """This function logs out a current user and removes the last entered location from the session"""

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

@app.route('/users')
def list_users():
    """This view function renders a page that lists users.

    It can take a 'q' param in querystring to search by a specific username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

        return render_template('users/user_list.html', users=users)

@app.route('/users/datelocations')
def show_date_locations():
    """This view function renders a page that shows the date locations according to the 
       location in the global flask environment and the users entered interest.
    """
    if not g.user:
        flash("Access Unauthorized, please login in!", "danger")
        return redirect("/")
    
    location = Location.query.get(session[CURR_LOCATION])

    return render_template('users/date_locations.html', location=location)


@app.route('/users/location/edit', methods=['GET', 'POST'])
def edit_location():
    """This view function is used to edit the user's location."""

    if  not g.user:
        flash("Access Unauthorized", "danger")
        return ("/")

    if not g.location:
        flash("Please enter location", "danger")
        return("/")

    location = g.location
    form=EditUserLocationForm(obj=location)

    if form.validate_on_submit():

        name = form.name.data
        address = form.address.data
        lat_lng_addy = get_lat_lng(GEOCODE_API_KEY, address)

        location.name=name,
        location.address=lat_lng_addy["full_address"]
        location.long=lat_lng_addy["longitude"]
        location.lat=lat_lng_addy["latitude"]
        
        db.session.commit()
        return redirect('/users/datelocations')

    return render_template('users/edit_location.html', form=form)
        




##################################################################################
# Homepage and error pages

@app.route('/', methods=['GET','POST'])
def homepage():
    """This view function takes you to the dateMeet homepage
    
    - anon users: no messages
    -logged in: 50 most recent posts by users if a city has not been entered. 
    
    """

    if g.user:
        if g.location:
            return redirect('/users/datelocations')

        form=UserLocationForm()

        if form.validate_on_submit():

            name = form.name.data
            address = form.address.data
            lat_lng_addy = get_lat_lng(GEOCODE_API_KEY, address)

            location = Location(
                name=name,
                address=lat_lng_addy["full_address"],
                long=lat_lng_addy["longitude"],
                lat=lat_lng_addy["latitude"],
                user_id = g.user.id

            )

            db.session.add(location)
            db.session.commit()

            session[CURR_LOCATION] = location.id

            return redirect('/users/datelocations')

        return render_template('home.html',form=form)

    else:
        return render_template('home-anon.html')

#######################################################################################
#Yelp Api requets 

@app.route('/dateMeet/api/yelp-business-search', methods=['POST'])
def retrieve_businesses():
    """This view function retrieves business information based on a existing location and 
        entered interest.
    """
   
    interest = request.json['interest']
    location = Location.query.get(session[CURR_LOCATION])
    address = location.address

    response = yelp_business_search(YELP_API_SECRET_KEY, address,interest)

    return jsonify(response)




