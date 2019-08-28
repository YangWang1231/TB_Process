# coding: utf-8
from sqlalchemy import Column, Enum, ForeignKey, Integer, LargeBinary, Table, Text, text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from TB_Process import login_manager
from TB_Process import app
from TB_Process import db
import os

#Base = declarative_base()
#metadata = Base.metadata


class GBJ8114Rule(db.Model):
    __tablename__ = 'GBJ8114_rule'

    id = Column(Integer, primary_key=True)
    GJB8114Code = Column(Text, unique=True)
    Rule_description = Column(Text, nullable=False)
    MandatoryStandard_ch = Column(Text)
    Rule_classification = Column(Enum('RECOMMENDED', 'MANDATORY', ''))


class LDRARule(db.Model):
    __tablename__ = 'LDRA_rule'

    id = Column(Integer, primary_key=True)
    LDRACode = Column(Text, unique=True)
    MandatoryStanard_en = Column(Text, nullable=False)


#t_sqlite_sequence = Table(
#    'sqlite_sequence', metadata,
#    Column('name', NullType),
#    Column('seq', NullType)
#)
class path_struct(object):
    def __init__(self, username = '', projectname = ''):
         if username is not '':
            self.base_path = os.path.join(app.config['USER_DATA_PATH'], username)
            self.temp_upload = os.path.join(self.base_path , 'temp_upload') #考虑删除该文件夹，直接将上传文件放入project/upload文件夹下
            self.extract = os.path.join(self.base_path,  'extracrt')
            if projectname is not '':
                self.projcet_floder = os.path.join(self.base_path, projectname)
                self.projcet_upload = os.path.join(self.projcet_floder, 'upload')
                self.project_result = os.path.join(self.projcet_floder,'result')
    



class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    password   = Column(Text)
    
    projects = db.relationship('Project', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    #make the basic floder structure for one user.  this should be one time operation
    @staticmethod
    def make_user_base_dir(username):
        path = path_struct(username)
        if not os.path.exists(path.base_path):
            os.mkdir(path.base_path)
            os.mkdir(path.temp_upload)
            os.mkdir(path.extract)
        return

    #make the projct floder structure, this operation will execute each project uploads
    @staticmethod
    def make_project_floder(username, projectname):
        path = path_struct(username, projectname)
        if not os.path.exists(path.projcet_floder):
            os.mkdir(path.projcet_floder)
            os.mkdir(path.projcet_upload)
            os.mkdir(path.project_result)
        return 

class GJBLDRARelationTable(db.Model):
    __tablename__ = 'GJB_LDRA_relation_table'

    id = Column(Integer, primary_key=True)
    GJB8114_id = Column(ForeignKey(u'GBJ8114_rule.id'), nullable=False)
    LDRA_id = Column(ForeignKey(u'LDRA_rule.id'), nullable=False)

    GJB8114 = relationship(u'GBJ8114Rule')
    LDRA = relationship(u'LDRARule')


class Project(db.Model):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    projectname = Column(Text, nullable=False)
    userid = Column(ForeignKey(u'user.id'), nullable=False)
    projectrowdata = Column(LargeBinary)
    processresult = Column(Text, server_default=text("'NOTSTART'"))

    #user = relationship(u'User')


class RuleObeyInfo(db.Model):
    __tablename__ = 'rule_obey_info'

    id = Column(Integer, primary_key=True)
    projectid = Column(ForeignKey(u'projects.id'), nullable=False)
    LDRA_Code = Column(ForeignKey(u'LDRA_rule.LDRACode'), nullable=False)
    location_function = Column(Text, nullable=False)
    line_numbers = Column(Text, nullable=False)

    LDRA_rule = relationship(u'LDRARule')
    project = relationship(u'Project')


class SourceFileInfo(db.Model):
    __tablename__ = 'source_file_info'

    id = Column(Integer, primary_key=True)
    projectid = Column(ForeignKey(u'projects.id'), nullable=False)
    sourcefilename = Column(Text, nullable=False)
    total_lines = Column(Integer, nullable=False)
    total_comments = Column(Integer, nullable=False)
    executeable_lines = Column(Integer, nullable=False)
    number_of_procedure = Column(Integer, nullable=False)

    project = relationship(u'Project')


class ComplextityMetricsInfo(db.Model):
    __tablename__ = 'complextity_metrics_info'

    id = Column(Integer, primary_key=True)
    file_id = Column(ForeignKey(u'source_file_info.id'), nullable=False)
    funtion_name = Column(Text, nullable=False)
    cyclomatic = Column(Integer, nullable=False)
    fan_out = Column(Integer, nullable=False)

    file = relationship(u'SourceFileInfo')



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))