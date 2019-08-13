#!/usr/bin/python
 #coding:utf-8
"""
 对后台数据进性建模，主要是User数据
 """

from TB_Process import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from TB_Process.config import Config
from store_db_sqlit3 import process_db

def get_User_by_name(username):
    user = User()
    db_path = Config.SQLALCHEMY_DATABASE_URI
    db_obj = process_db(db_path)
    id, name, password = db_obj.get_user_by_name(username)
    if id is not -1:
        user.id = id
        user.username = name
        user.password_hash = "433808" #fake
        return user
    else:
        return None


def get_User_by_id(id):
    user = User()
    db_path = Config.SQLALCHEMY_DATABASE_URI
    db_obj = process_db(db_path)
    id, name, password = db_obj.get_user_by_id(int(id))
    if id is not -1:
        user.id = id
        user.username = name
        user.password_hash = "433808" #fake
        return user
    else:
        return None

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
        #return check_password_hash(self.password_hash, password)
        return True  #fake


@login.user_loader
def load_user(id):
    return get_User_by_id(id)
