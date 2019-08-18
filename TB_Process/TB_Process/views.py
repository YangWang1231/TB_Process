#!/usr/bin/python
 #coding:utf-8
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user
from flask_login import logout_user
from TB_Process import app
from TB_Process.forms import LoginForm
from TB_Process.forms import UploadForm
import TB_Process.store_db_sqlit3
from TB_Process.models import get_User_by_name

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_User_by_name(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register')
def register():
    """Renders the register page."""
    return "this is register page, to be complete."


#@app.route('/home' , methods=['POST'])
@app.route('/', methods=['GET', 'POST'])
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
#            filename = secure_filename(file.filename.encode('utf-8'))
            #savepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            savepath = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('uploaded_file', filename=file.filename))
        else:
             flash('file type is not allowed.')
        return "1"
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

from jinja2 import Template
@app.route('/personpage')
def personpage():
    """Renders the contact page."""
    template = Template('<H1>Hello {{ name }}!</H1>')
    string = template.render(name = current_user.username)
    return string

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

import os
from TB_Process.config import Config
from werkzeug import secure_filename
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
#            filename = secure_filename(file.filename.encode('utf-8'))
            #savepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            savepath = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('uploaded_file', filename=file.filename))
        else:
             flash('file type is not allowed.')
    return "1"
    #return render_template('upload.html', title='uploadfile')

@app.route('/upload_tbsystem', methods=['POST'])
def upload_tb_system():
    form_tb_system = UploadForm()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #不能处理中文文件名
            #处理方法见 ’secure_filename 对中文不支持的处理‘
#            filename = secure_filename(file.filename.encode('utf-8'))
            #savepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            savepath = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('uploaded_file', filename=file.filename))
        else:
             flash('file type is not allowed.')
    return render_template('upload.html', title='uploadfile')


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)