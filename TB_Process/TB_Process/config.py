import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'flaskr.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        os.path.join(basedir, 'flaskr.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = r'C:\Users\Administrator\source\repos\TB_Process\TB_Process\TB_Process\uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'rar', 'zip', 'jpg', 'jpeg', 'gif'])