#!/usr/bin/env python3
'''
   Configuration module
'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    '''
       Configuration class
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    MAIL_SERVER = os.environ.get('MAIL_server')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSSWORD')
    ADMINS = ['duma_sphesihle@gmail.com']

