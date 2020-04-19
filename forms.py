from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[InputRequired(), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
        'Usernames must must have only letters, numbers and underscores')])
    email = EmailField('Email',
        validators=[InputRequired(), Email()])
    password = PasswordField('Password',
        validators=[InputRequired(), Length(min=3, max=8)])
    confirm_password = PasswordField('Confirm Password',
        validators=[InputRequired(), EqualTo('password', message = 'Passwords must match')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = EmailField('Email',
        validators=[InputRequired(), Email()])
    password = PasswordField('Password',
        validators=[InputRequired()])
    submit = SubmitField('Log In')

class ConferenceForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Regexp('^[A-Za-z][A-Za-z]*$', 0,
        'Usernames must must have only letters. No spaces')])
    email = EmailField('Email',validators=[InputRequired(), Email()])
    date = StringField('Date(YYYY-MM-DD)',validators=[InputRequired()])
    send = SubmitField('Send')

class ForgotForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('New Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')
