from flask import Flask, render_template, url_for, flash, redirect, request
from netbank import app, db, bcrypt
from netbank.models import User
from netbank.forms import RegistrationForm, LoginForm, SendMoneyForm
from flask_login import login_user, current_user, logout_user, login_required
from wtforms.validators import  ValidationError


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
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('logged_in_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)#, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('logged_in_page'))
        else:
            flash('Login Unsuccessful. Please check username and password ', 'danger')
    return render_template('login_page.html', title='Login', form=form)

@app.route('/logged_in_page', methods=['GET', 'POST'])
@app.route('/logged_in_page.html', methods=['GET', 'POST'])
@login_required
def logged_in_page():
    form = SendMoneyForm()
    list_of_users = []
    all_users = User.query.all()
    for users in all_users:
        if current_user != users:
            list_of_users.append(users.username)
    form.recipient.choices = list_of_users

    #money sending
    if form.validate_on_submit():
        user_recieve = User.query.filter_by(username=form.recipient.data).first()
        user_send = current_user
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