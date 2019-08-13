"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user
from flask_login import logout_user
from TB_Process import app
from TB_Process.forms import LoginForm
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

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
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
