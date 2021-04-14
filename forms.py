"""This file holds the structure of all forms to be utilized in the dateMeet app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

class UserRegisterForm(FlaskForm):
    """Form for registering a new user"""

    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=30)])
    image_url = StringField('(Optional) Image Url', validators=[Optional()])

class UserEditForm(FlaskForm):
    """Form for editing user information."""

    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8, max=30)])
    image_url = StringField('(Optional) Image Url', validators=[Optional()])
    bio = TextAreaField('(Optional) Tell dateMeet users about yourself', validators=[Optional()])

class UserLoginForm(FlaskForm):
    """Login form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8, max=30)])

class UserLocationForm(FlaskForm):
    """This class holds the structure of a location and interest form for the user"""

    name = StringField('Save Location as', validators=[Optional()])
    address = StringField('Enter current address', validators=[DataRequired()])


     

    