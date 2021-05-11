"""This file holds the structure of all forms to be utilized in the dateMeet app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.widgets import html5

class UserRegisterForm(FlaskForm):
    """Form for registering a new user"""

    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=30)])
    image_url = StringField('(Optional) Image Url', validators=[Optional()])
    header_url = StringField('(Optional) Header Url', validators=[Optional()])

class UserEditForm(FlaskForm):
    """Form for editing user information."""

    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=30)])
    image_url = StringField('(Optional) Image Url', validators=[Optional()])
    header_url = StringField('(Optional) Header Url', validators=[Optional()])
    bio = TextAreaField('(Optional) Tell dateMeet users about yourself', validators=[Optional()])

class UserLoginForm(FlaskForm):
    """Login form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8, max=30)])

class UserLocationForm(FlaskForm):
    """This class holds the structure of a location form for the user"""

    name = StringField('Save Location as', validators=[DataRequired()])
    address = StringField('Enter current address', validators=[DataRequired()])

class EditUserLocationForm(FlaskForm):
    """This class holds the structure of the edit location form for a user"""

    name = StringField('Save Location as', validators=[DataRequired()])
    address = StringField('Enter current address', validators=[DataRequired()])


class UserRecommendationAddForm(FlaskForm):
    """This class holds the structure of the create recommendation form for a user"""

    title = StringField('Title', validators=[DataRequired(), Length(max=250)])
    content = StringField('Content', validators=[DataRequired(), Length(max=500)])
    business_name = StringField('Business Name', validators=[DataRequired()])
    business_address = StringField('Business Address', validators=[DataRequired()])
    business_city = StringField('Business City', validators=[DataRequired()])
    business_state = StringField('Business State', validators=[DataRequired()])
    business_country = StringField('Business Country', validators=[DataRequired()])
    business_rating = IntegerField('Business Rating(1-5)', widget=html5.NumberInput(min = 1, max = 5))

class UserRecommendationEditForm(FlaskForm):
    """This class holds the structure of the create recommendation form for a user"""

    title = StringField('Title', validators=[DataRequired(), Length(max=250)])
    content = StringField('Content', validators=[DataRequired(), Length(max=500)])
    business_name = StringField('Business Name', validators=[DataRequired()])
    business_address = StringField('Business Address', validators=[DataRequired()])
    business_city = StringField('Business City', validators=[DataRequired()])
    business_state = StringField('Business State', validators=[DataRequired()])
    business_country = StringField('Business Country', validators=[DataRequired()])
    business_rating = IntegerField('Business Rating(1-5)', widget=html5.NumberInput(min = 1, max = 5))
    
  
    
     

    