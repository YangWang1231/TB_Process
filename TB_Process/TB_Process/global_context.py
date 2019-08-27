#!/usr/bin/python
#coding:utf-8
"""
本模块封装了全局可使用资源，并且负责回收资源
"""

from flask import g
from TB_Process import app

def set_path(path):
    g.path = path
    return 

def get_path():
    return g.path

@app.teardown_appcontext
def teardown_db(exception):
    #just test when to call
    pass

@app.teardown_request
def teardown_req(exception):
    pass