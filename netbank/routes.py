from flask import Flask, render_template, url_for, flash, redirect
from netbank import app, db, bcrypt
from netbank.models import User
from netbank.forms import RegistrationForm, LoginForm

db.drop_all()
db.create_all()

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register.html', methods=['GET', 'POST'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data))
        return redirect(url_for('logged_in_page'))
    return render_template('login_page.html', title='Log In', form=form)


@app.route('/logged_in_page.html')
def logged_in_page():
    return render_template('logged_in_page.html')