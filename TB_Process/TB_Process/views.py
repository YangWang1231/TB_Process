"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, send_from_directory, flash, redirect
from TB_Process import app
from TB_Process.forms import LoginForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renders the login page."""
    form = LoginForm()
    if form.validate_on_submit():
            flash('Login requested for user {}, remember_me={}'.format(
                form.username.data, form.remember_me.data))
            return redirect('/home')
    return render_template('login.html', title='Sign In', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login2():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


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

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
