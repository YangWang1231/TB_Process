#!/usr/bin/python
 #coding:utf-8

"""
The flask application package.
"""

from flask import Flask
from flask_login import LoginManager
from .config import Config


app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

import TB_Process.views, TB_Process.models
