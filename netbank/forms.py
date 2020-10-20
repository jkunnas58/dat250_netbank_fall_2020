from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError
from netbank.models import User
from flask_login import current_user
import safe


class RegistrationForm(FlaskForm):
    #TODO update minimum lengths on username and password
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    amount = IntegerField('Insert Amount $ 100-1000', 
                        validators=[DataRequired(), NumberRange(min= 100, max=1000, message='Must be between 100 and 1000')])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    # def validate_money(self, amount):
    #     if amount > 1000 or amount< 100:
    #         if type(amount) is not int:
    #             raise ValidationError('Money amount must be between 100 and 1000')

    def validate_password(self, password):
        password_check = safe.check(password.data, min_types = 2)
        if not password_check:
            raise ValidationError('Password is not secure. Please have at least 8 Characters including numbers and letters')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])    
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    # uncommenting this will let you know if you have entered a valid password and leave it more vunerable for brute force attacks 
    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if not user:
    #         raise ValidationError('That username does not exist. Please check spelling')
    


class SendMoneyForm(FlaskForm):    
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=1, message='Must be a valid number between 1 and you account amount')])
    recipient = SelectField(label='Recipient', choices=[])
    submit = SubmitField('Send Money')
    username = StringField('Username', validators=[DataRequired()])  
    password = PasswordField('Password', validators=[DataRequired()])

    # def validate_amount(self, amount):
    #     if type(amount) is not int:
    #         raise ValidationError('Amount must be a valid integer number')

    