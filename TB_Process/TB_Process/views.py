"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, send_from_directory
from TB_Process import app

@app.route('/Login_v14/login')
def login():
    """Renders the login page."""
    return render_template('login.html')

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
