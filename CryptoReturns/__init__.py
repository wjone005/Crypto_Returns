# Python standard libraries
import os
from flask import Flask
from os import environ as env
# Import SQL
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__)

# Location where database will be and created
# /// means relative path from current file
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
application.config['SESSION_COOKIE_SECURE'] = False

# SQLAlchemy instance
db = SQLAlchemy(application)







# Place here to prevent circular import error
from CryptoReturns import routes