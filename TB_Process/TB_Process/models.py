#!/usr/bin/python
 #coding:utf-8
"""
 对后台数据进性建模，主要是User数据
 """

#from TB_Process import login_manager
#from flask_login import UserMixin
#from werkzeug.security import generate_password_hash, check_password_hash
#from TB_Process.config import Config
#from TB_Process.store_db_sqlit3 import process_db
#from TB_Process import db


#class User_ORM(db.Model):
#    __tablename__ = 'user'

#def get_User_by_name(username):
#    db_path = Config.SQL_DATABASE_URI
#    db_obj = process_db(db_path)
#    id, name, password = db_obj.get_user_by_name(username)
#    if id is not -1:
#        user = User()
#        user.id = id
#        user.username = name
#        user.password_hash = password
#        return user
#    else:
#        return None


#def get_User_by_id(id):
#    db_path = Config.SQL_DATABASE_URI
#    db_obj = process_db(db_path)
#    id, name, password = db_obj.get_user_by_id(int(id))
#    if id is not -1:
#        user = User()
#        user.id = id
#        user.username = name
#        user.password_hash = password
#        return user
#    else:
#        return None

#class User(UserMixin):
#    def __init__(self, username = ""):
#        self.id = 0
#        self.username = username
#        self.password_hash = ""

#    def __repr__(self):
#        return '<User {}>'.format(self.username)

#    def set_password(self, password):
#        self.password_hash = generate_password_hash(password)

#    def check_password(self, password):
#        return check_password_hash(self.password_hash, password)
#        #return True  #fake

#    def get_id(self):
#        return unicode(self.id)

#    def store_to_db(self):
#        db_path = Config.SQL_DATABASE_URI
#        db_obj = process_db(db_path)
#        db_obj.insert_user((self.username, self.password_hash))
#        db_obj.commit()


#@login_manager.user_loader
#def load_user(id):
#    return get_User_by_id(id)

