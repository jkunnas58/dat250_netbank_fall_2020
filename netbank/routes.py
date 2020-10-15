from flask import Flask, render_template, url_for, flash, redirect
from netbank import app, db, bcrypt
from netbank.models import User
from netbank.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user

db.drop_all()
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
            return redirect(url_for('logged_in_page'))
        else:
            flash('Login Unsuccessful. Please check username and password ', 'danger')
    return render_template('login_page.html', title='Login', form=form)


@app.route('/logged_in_page.html')
def logged_in_page():
    if current_user.is_authenticated:
        return render_template('logged_in_page.html', title='Logged_in')
    else:
        return redirect(url_for('login_page'))
    # return render_template('logged_in_page.html', title='Logged_in')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))