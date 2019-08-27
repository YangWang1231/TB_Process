#!/usr/bin/python
 #coding:utf-8

"""
The flask application package.
"""

from flask import Flask
from flask_login import LoginManager
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



import TB_Process.views, TB_Process.models, TB_Process.module
