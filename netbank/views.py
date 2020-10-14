from flask import Flask, render_template, url_for, flash, redirect
from netbank import app , db
from netbank.forms import RegistrationForm, LoginForm
# from flask_login import LoginManager

db.drop_all()
db.create_all()

app.config['SECRET KEY'] = '1x5y4-4ds7f-4fk76' #need to input secret key


def check_register_amount(money_input):
    if type(money_input) is int:
        if money_input <= 1000:
            if money_input >= 100:
                return True
    else:
        return False
