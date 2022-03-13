from ..models import User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Email,EqualTo, Length, DataRequired
from wtforms import ValidationError

    
    
class RegForm(FlaskForm):
    username = StringField('Enter Your Username', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators = [DataRequired(), EqualTo('password_confirm', message = 'Passwords should match'), Length(min=8, max=15,)])
    password_confirm = PasswordField('Confirm Passwords',validators = [DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError(message="The Email you entered has already been taken!")
    
    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError(message="The username has already been taken, choose another username")

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me!')
    submit = SubmitField('Login')
