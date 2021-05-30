# Python standard libraries
import os
from flask import Flask

# Import SQL
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

# Location where database will be and created
# /// means relative path from current file
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
application.config['SECRET_KEY'] = os.urandom(24)

# SQLAlchemy instance
db = SQLAlchemy(application)

# Place here to prevent circular import error
from CryptoReturns import routes