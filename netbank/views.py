from flask import Flask, render_template, url_for, flash, redirect
from netbank import app #, query_db
from forms import RegistrationForm, LoginForm

app.config['SECRET KEY'] = '' #need to input secret key

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # if form.validate_on_submit()
        # flash(f'Account created for {form.username.data}', 'success')
        # return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login_page.html')
def login_page():
    form = LoginForm()
    return render_template('login_page.html', form=form)

@app.route('/logged_in_page.html')
def logged_in_page():
    return render_template('logged_in_page.html')
