#!/usr/bin/env python3
'''
   Form module accepting user input
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from mainapp import db
from mainapp.models import User


class LoginForm(FlaskForm):
    '''
       Login form class
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    ''' Registration form to register users
    '''
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        ''' Validating the username
        '''
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        '''
           Validating the email address
        '''
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
