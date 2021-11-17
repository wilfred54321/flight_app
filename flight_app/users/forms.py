from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,EmailField,PasswordField
from wtforms import validators
from wtforms.validators import DataRequired,Email,Length,ValidationError,EqualTo
from flight_app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),Length(min = 5, max = 20)])
    firstname = StringField('Firstname', validators = [DataRequired(), Length(min = 2 , max = 20)])
    lastname = StringField('Lastname', validators = [DataRequired(), Length(min = 2 , max = 20)])
    email = EmailField('Email', validators = [DataRequired(), Email()] )
    submit = SubmitField('Create Agent')



    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken, Please choose a different username')



    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken , Please choose another email address')



class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if not user:
            raise ValidationError('That username does not exist, Please choose a different username')



class SetPasswordForm(FlaskForm):
    default_password = StringField('Default Password', validators= [DataRequired(), Length(min = 7, max = 7)])
    password = PasswordField('New Password', validators = [DataRequired(),Length(min=8)])
    confirm_password = PasswordField('Confirm Password' ,validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Set Password')

   
   