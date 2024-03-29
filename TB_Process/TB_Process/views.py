#!/usr/bin/python
 #coding:utf-8
"""
Routes and views for the flask application.
"""
import os
from datetime import datetime
from jinja2 import Template
from flask import render_template, flash, redirect, url_for, request
from flask import session
from flask import send_from_directory
from flask_login import current_user, login_user, logout_user
from TB_Process import app
from TB_Process.forms import LoginForm, RegistrationForm, UploadForm
import TB_Process.store_db_sqlit3
from TB_Process.module import User, Project
from TB_Process.process_upload import Process_Html_Report
from TB_Process.config import Config
from werkzeug import secure_filename
from TB_Process.process_upload import Process_Html_Report
from TB_Process import db
from TB_Process.module import path_struct
from TB_Process.global_context import set_path, get_path
from TB_Process.unpack import unzip_file
import json
from sqlalchemy import and_


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        #user = get_User_by_name(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        #make user dir, should be done when user register
        User.make_user_base_dir(user.name)

        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Renders the register page."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name = form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        #make user dir, should be done when user register
        User.make_user_base_dir(user.name)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


from thread import start_new_thread
import time
#from TB_Process.test_thread import call_fun

#@app.route('/home' , methods=['POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """Renders the home page."""
    form_source = UploadForm()
    form_tb_system = UploadForm()

    #debug string
    #templates = Template('{{form.file }}')
    #str_render = templates.render(form_source = form_source, form_tb_system = form_tb_system)
    #end debug
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #不能处理中文文件名
            #处理方法见 ’secure_filename 对中文不支持的处理‘
            #filename = secure_filename(file.filename.encode('utf-8'))
            #savepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            savepath = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            unzip_file(os.path.join(app.config['UPLOAD_FOLDER'], file.filename) ,  app.config['EXTRACT_FOLDER'])
            #debug code: test the lifecycle of the flask thread. it seems that one server run, then keeps a thread, not quite, so the sub thread runs forever.
            #call_fun()
            return "1"
        else:
             return "0"
    else:
        return render_template(
            'index.html',
            title='Home Page',
            year=datetime.now().year,
            form_source = form_source, 
            form_tb_system = form_tb_system
        )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


def allowed_file(filename):
    #anotherfilename = filename.encode('utf-8')
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS

#不需要处理get请求，因为给请求已经通过index页面解决了
#@app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload_source', methods=['POST'])
def upload_source_code():
    form = UploadForm()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #不能处理中文文件名
            #处理方法见 ’secure_filename 对中文不支持的处理‘
            #filename = secure_filename(file.filename.encode('utf-8'))
            #savepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            savepath = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('uploaded_file', filename=file.filename))
        else:
             flash('file type is not allowed.')
    return "1"
    #return render_template('upload.html', title='uploadfile')


import thread
def process_tb_system_fun(system_zip_floder, path, project_obj):
    processfile = Process_Html_Report()
    processfile.process_tb_system(system_zip_floder, path) 
    metrix_file = processfile.get_metrix_result_path()
    rule_file = processfile.get_rule_result_path()
    project_obj.process_status = 'Finished'
    db.session.add(project_obj)
    db.session.commit()
    return 


'''
process request for project status
input:
{
    'projectname' :  'xxxx'
}
return:
type: string
"None": can not find row in DB, should not happen
"Finished"
"Processing"
"NOTSTART"
'''
@app.route('/project_status', methods=['GET'])
def get_project_status():
    prj_name=request.args.get('projectname')
    prj_obj = Project.query.filter_by(projectname = prj_name).first()
    
    dic = {"status":"", "filename":""}
    if not prj_obj:
        dic['status'] = "None" #should not happen
    elif prj_obj.process_status == "Finished":
        dic['status'] = prj_obj.process_status
        dic["filename"] = "demo.docx"
    else:
        dic['status'] = prj_obj.process_status

    return json.dumps(dic)

    
    #debug
    if 'access_count' not in session:
        session['access_count'] = 1
    else:
        session['access_count'] = session['access_count'] + 1
    
    if session['access_count'] >= 10:
        return 'Finished'
    return 'Processing'

'''
process upload floder which contain a testbed system project contents
'''
@app.route('/upload_tbsystem', methods=['POST'])
def upload_tb_system():
    form_tb_system = UploadForm()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #save file to USER_DATA_PATH/user/temp_upload
            userinstance = current_user._get_current_object() 
            path = path_struct(userinstance.name, form_tb_system.project_name.data)
            #session中只能保存dictionary对象，因为session会保存在client端，所以需要jison类型才能发送
            #或者，写一个path类的jison化、反jison化函数也可以
            session['current_project_name'] = form_tb_system.project_name.data
            session['current_user'] = userinstance.name
            User.make_project_floder(userinstance.name, form_tb_system.project_name.data)
            file.save(os.path.join(path.projcet_upload, file.filename))
            #先建立工程的DB条目，并且project的初始状态为Processing
            project = Project( projectname = form_tb_system.project_name.data, 
                                user = userinstance, process_status = 'Processing', date = datetime.now(), project_path = path.project_alternative_path)
            db.session.add(project)
            db.session.commit()
            #mutile thread
            thread.start_new_thread( process_tb_system_fun, (os.path.join(path.projcet_upload, file.filename), path, project, ) )
            return "1"

            ##sequence execute
            ##comment block
            ##extract to function
            ##long time process, should be send to another thread
            #processfile = Process_Html_Report()
            #processfile.process_tb_system(os.path.join(path.projcet_upload, file.filename), path) 

            #metrix_file = processfile.get_metrix_result_path()
            #project = Project( projectname = form_tb_system.project_name.data, 
            #                            user = userinstance)
            #db.session.add(project)
            #db.session.commit()
            ##end: extract to function

            #return redirect(url_for('uploaded_file', filename=metrix_file))
            ###待解决：直接调用send_from_directiory函数，下载的文件名称不正确，使用redirect_url方式，下载的文件名称正确。。
            ###return send_from_directory(app.config['RESULT_FOLDER'], metrix_file)
            ##end comment block

        else:
             flash('file type is not allowed.')
    return render_template('upload.html', title='uploadfile')

from flask_login import logout_user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
#    path = path_struct(session['current_user'] , session['current_project_name'] )
#    return send_from_directory(path.project_result, filename)

@app.route('/uploads')
def uploaded_file():
    filename=request.args.get('metrics_filename')
    path = path_struct(session['current_user'] , session['current_project_name'] )
    return send_from_directory(path.project_result, filename, as_attachment=True)


#no use currently
def generate_table_value(projects):
    items = []
    for project in projects:
        an_item = dict(date=project.date, projectname=project.projectname , Status=project.process_status, Uploads = "upload floder", Results ="Result floder", value ="waiting")
        items.append(an_item)

    return items

@app.route('/personalpage')
def personalpage():
    page = request.args.get('page', 1, type=int)
    user = current_user._get_current_object()
    project_pagination = Project.query.filter_by(user = user).paginate(
            page, per_page=app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    if len(project_pagination.items) == 0:
        return render_template('project_info.html')
    
    items = project_pagination.items
    return render_template('project_info.html', items = items, pagination=project_pagination)


def compress_floderfiles(floder_path):
    '''compress all files under a floder'''
    import zipfile
    
    filelist = os.listdir(floder_path)
    with zipfile.ZipFile(os.path.join(floder_path,app.config['ANALYSE_RESULT_FILENAME']), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in filelist:
            zipf.write(os.path.join(floder_path, file), file)

    return 'result.zip'



def get_download_filepath(projectname, flodername):
    '''retrive floder path from DB get floder from file system
    Args:
        projectname: current project name in DB-projects table
        flodername: 'result' or 'upload'
    return value: 
        file_path: the path of download file(must be a rar/zip file)
    '''
    user = current_user._get_current_object()
    cur_prj = db.session.query(Project).filter(and_(user.id == Project.userid, Project.projectname == projectname)).first()
    prj_path = os.path.join(app.config['USER_DATA_PATH'], cur_prj.project_path) 
    file_path = os.path.join(prj_path,flodername)
    return file_path

@app.route('/result_floder/<projectname>', methods=['GET'])
def get_result_floder(projectname):
    file_path = get_download_filepath(projectname, 'result')
    if app.config['ANALYSE_RESULT_FILENAME'] not in os.listdir(file_path):
        compress_floderfiles(file_path)
    return send_from_directory(file_path, app.config['ANALYSE_RESULT_FILENAME'], as_attachment=True)


@app.route('/upload_floder/<projectname>', methods=['GET'])
def get_upload_floder(projectname):
    get_download_filepath(projectname, 'upload')
    filename = os.listdir(file_path)
    return send_from_directory(file_path, filename[0], as_attachment=True)


    