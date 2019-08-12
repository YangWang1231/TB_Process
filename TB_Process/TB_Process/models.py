#!/usr/bin/python
 #coding:utf-8
"""
 对后台数据进性建模，主要是User数据
 """

from TB_Process import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self):
        self.id = 0
        self.username = ""
        self.password_hash = ""

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    user_fake = User()
    user_fake.id = 1
    user_fake.username = u'王洋'
    return user_fake
   # return User.query.get(int(id))