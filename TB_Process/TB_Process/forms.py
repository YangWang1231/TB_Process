 #coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from TB_Process.models import User


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

from flask_wtf.file import FileField, FileRequired, FileAllowed
class UploadForm(FlaskForm):
    file = FileField(validators=[
        #file allowed 没有起作用，可以上传各种类型的文件，在config.py的ALLOWED_EXTENSIONS字段中的内容才起作用
        FileAllowed(['rar', 'zip'], u'Only rar files'), 
        FileRequired(u'not choican a file')])
    submit = SubmitField(u'Upload')