 #coding:utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'flaskr.sqlite')
    SQL_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        os.path.join(basedir, 'flaskr.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_DATA_PATH = os.getcwd() + r'\TB_Process\User_Data'
    UPLOAD_FOLDER = os.getcwd() + r'\TB_Process\uploads'
    EXTRACT_FOLDER = os.getcwd() + r'\TB_Process\extract_floder'    
    RESULT_FOLDER = os.getcwd() + r'\TB_Process\result_floder'    
    ALLOWED_EXTENSIONS = set(['rar', 'zip'])
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024 #max upload file : 50M
    UPLOAD_FILE_EXTENSION = ['.rar', '.zip']
    UNRAR_FILE_PATH = r'C:\Program Files\WinRAR\Unrar'
    REPORT_TEMPLATE_PATH =  r'C:\Users\Administrator\source\repos\TB_Process\TB_Process\TB_Process\analyse_html'
    METRICS_REPORT_TEMPLATE = u'质量度量.docx'
    RULE_REPORT_TEMPLATE = u'规则模板.docx'
    FLASKY_POSTS_PER_PAGE = 10
    ANALYSE_RESULT_FILENAME = 'result.zip'