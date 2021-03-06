from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, ValidationError
from netbank.models import User
from flask_login import current_user
import safe


class RegistrationForm(FlaskForm):
    """

    """
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    amount = IntegerField('Insert Amount $ 100-1000', 
                        validators=[DataRequired(), NumberRange(min= 100, max=1000, message='Must be between 100 and 1000')])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_password(self, password):
        password_check = safe.check(password.data, length=8, min_types = 4, level=3)
        if not password_check:
            raise ValidationError('Password is not secure. Please have at least 8 Characters including numbers, one special symbol and upper and lower case letters')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])    
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

   


class SendMoneyForm(FlaskForm):    
    amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min=1, message='Must be a valid number between 1 and you account amount')])
    # recipient = SelectField(label='Recipient', choices=[])
    recipient2 = IntegerField('Account Number', validators=[DataRequired()])
    submit = SubmitField('Send Money')
    username = StringField('Username', validators=[DataRequired()])  
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_acount(self, recipient2):
        user = User.query.filter_by(id=recipient2.data).first()
        if not user:
            raise ValidationError('That account does not exist. Please check the number')

    