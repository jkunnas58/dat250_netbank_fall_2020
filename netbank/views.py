from flask import Flask, render_template, url_for, flash, redirect
from netbank import app , db
db.create_all()
# from forms import RegistrationForm, LoginForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


app.config['SECRET KEY'] = '1x5y4-4ds7f-4fk76' #need to input secret key

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=8, max=20)])
    
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')



@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login_page')
@app.route('/login_page.html')
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data))
        return redirect(url_for('index'))
    return render_template('login_page.html', title='Log In', form=form)


@app.route('/logged_in_page.html')
def logged_in_page():
    return render_template('logged_in_page.html')