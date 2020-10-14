import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1x5y4-4ds7f-4fk76'