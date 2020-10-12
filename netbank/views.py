from flask import render_template
from netbank import app #, query_db


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/login_page.html')
def login_page():
    return render_template('login_page.html')

@app.route('/logged_in_page.html')
def logged_in_page():
    return render_template('logged_in_page.html')