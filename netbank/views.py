from flask import Flask
from flask import render_template
from netbank import app #, query_db
from forms import LoginForm

app.config['SECRET KEY'] = '5791628bb0b13ce0c677dfde280ba245'

@app.route('/')
def index():
    # articles = query_db('SELECT rowid, * FROM article;')
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    #form = LoginForm()
    return render_template('login_page.html', title='Login') #, form=form)

@app.route('/logged_in_page')
def logged_in_page():
    return render_template('logged_in_page.html', title='You are now logged in')


# @app.route('/article/<int:article_id>')
# def article(article_id):
#     article = query_db(
#         'SELECT * FROM article WHERE id=?;', (str(article_id)), True)
#     return render_template('article.html', article=article)