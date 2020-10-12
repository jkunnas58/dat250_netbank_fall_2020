from flask import render_template
from netbank import app #, query_db


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('login_page.html')

@app.route('/logged_in_page')
def logged_in_page():
    return render_template('logged_in_page.html')