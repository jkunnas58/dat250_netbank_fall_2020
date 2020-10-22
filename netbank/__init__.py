from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '958efa56da92ed114e48d8b256eebeffdbcb24f30bf6d500'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#for local database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#for local postgresql database TODO
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#for Heroku postgresql deployment
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.session_protection = "strong"
limiter = Limiter(
            app,
            key_func= get_remote_address,
            default_limits=["200 per day", "50 per hour"]
)


from netbank import routes
