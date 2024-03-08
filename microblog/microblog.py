#!/usr/bin/env python3
'''
   This is a module run the application
'''
from mainapp import app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from mainapp.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}
