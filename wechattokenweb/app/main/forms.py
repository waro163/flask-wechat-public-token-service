# -*- coding: utf-8 -*-

from flask_wtf import Form,FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,FileField
from wtforms.validators import DataRequired,Required,Length,Email,EqualTo,Regexp
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed,FileRequired
from flask import current_app

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    name = StringField('What is your name?')
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

