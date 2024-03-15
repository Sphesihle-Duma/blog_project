#!/usr/bin/env python3
'''
   Module for handlers
   it imports app which is a member of 
   the package.
   creates supported routes
'''
from mainapp import app, db
from flask import render_template, flash, redirect, url_for, request
from mainapp.forms import LoginForm
from flask_login import current_user, login_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from mainapp.models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    '''
       view function for home page
    '''
    user = {'username': 'Sphesihle'}
    posts = [
            {
                'author' : {'username': 'Mandla'},
                'body': 'Beautiful day in Portland'
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The avengers movie was so cool!'
            }
            ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
       login view
    '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
                sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    '''
       Logging out the user view
    '''
    logout_user()
    return redirect(url_for('index'))
