from flask import render_template
from netbank import app #, query_db


@app.route('/')
def index():
    # articles = query_db('SELECT rowid, * FROM article;')
    return f"<h1>Hello world</h1>"


# @app.route('/article/<int:article_id>')
# def article(article_id):
#     article = query_db(
#         'SELECT * FROM article WHERE id=?;', (str(article_id)), True)
#     return render_template('article.html', article=article)
