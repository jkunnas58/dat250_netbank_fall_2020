from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError
from netbank.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    #TODO update minimum lengths on username and password
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    amount = IntegerField('Insert Amount $ 100-1000', 
                        validators=[DataRequired(), NumberRange(min= 100, max=1000, message='Must be between 100 and 1000')])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2,max=60)])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    # def validate_money(self, amount):
    #     if amount > 1000 or amount< 100:
    #         if type(amount) is not int:
    #             raise ValidationError('Money amount must be between 100 and 1000')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('That username does not exist. Please check spelling')
    


class SendMoneyForm(FlaskForm):    
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=1, message='Must be a valid number between 1 and you account amount')])
    recipient = SelectField(label='Recipient', choices=[])
    submit = SubmitField('Send Money')

    # def validate_amount(self, amount):
    #     if type(amount) is not int:
    #         raise ValidationError('Amount must be a valid integer number')

    