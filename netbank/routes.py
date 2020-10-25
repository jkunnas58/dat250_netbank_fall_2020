from flask import Flask, render_template, url_for, flash, redirect, request, session
from netbank import app, db, bcrypt, limiter
from netbank.models import User
from netbank.forms import RegistrationForm, LoginForm, SendMoneyForm
from flask_login import login_user, current_user, logout_user, login_required
from wtforms.validators import  ValidationError
from datetime import timedelta


# db.drop_all() #uncomment this if you want a clean database everytime you restart server
db.create_all()

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, account=form.amount.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}, you can now login', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', form=form)


@app.route('/login_page', methods=['GET', 'POST'])
@app.route('/login_page.html', methods=['GET', 'POST'])
@limiter.limit("5/5minute")
def login_page():
    #checks if the current user is logged in, will then redirect to logged in page
    if current_user.is_authenticated:
        return redirect(url_for('logged_in_page'))
    form = LoginForm()

    #if form is valid, it will check is user is in database and check the password is correct using the bcrypt function of checking hashed password.
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)#, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('logged_in_page'))
        else:
            flash('Login Unsuccessful. Please check username and password ', 'danger')
    else:
        return render_template('login_page.html', title='Login', form=form)
    return render_template('login_page.html', title='Login', form=form)

@app.route('/logged_in_page', methods=['GET', 'POST'])
@app.route('/logged_in_page.html', methods=['GET', 'POST'])
@login_required
def logged_in_page():
    form = SendMoneyForm()
    #code for timing out the logged in page
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=2)

    #money sending
    if form.validate_on_submit():
        user_recieve = User.query.filter_by(id=form.recipient2.data).first()       
        if form.amount.data <= current_user.account:
            current_user.account -= form.amount.data
            user_recieve.account += form.amount.data
            db.session.commit()      
            flash('Sending of money successful', 'success')
            return redirect(url_for('logged_in_page'))
        else:
                flash('Insufficient funds, please select an amount you have available in your account', 'error')

    else:
        pass


    return render_template('logged_in_page.html', title='Logged_in', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))