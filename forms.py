from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import InputRequired

class RegisterUser(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email address') 
    first_name = StringField('First name')
    last_name = StringField('Last name')
    
class Login(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])