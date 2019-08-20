import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'flaskr.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        os.path.join(basedir, 'flaskr.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #UPLOAD_FOLDER = r'C:\Users\Administrator\source\repos\TB_Process\TB_Process\TB_Process\uploads'
    UPLOAD_FOLDER = os.getcwd() + r'\TB_Process\uploads'
    EXTRACT_FOLDER = os.getcwd() + r'\TB_Process\extract_floder'    
    RESULT_FOLDER = os.getcwd() + r'\TB_Process\result_floder'    
    ALLOWED_EXTENSIONS = set(['txt', 'rar', 'zip', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024 #max upload file : 50M
    UPLOAD_FILE_EXTENSION = ['.rar', '.zip']
    UNRAR_FILE_PATH = r'C:\Program Files\WinRAR\Unrar'
    #unrar_file_path = r'C:\Program Files\WinRAR\Unrar'