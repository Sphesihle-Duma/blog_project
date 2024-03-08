#!/usr/bin/env python3
'''
   Module for handlers
   it imports app which is a member of 
   the package.
   creates supported routes
'''
from mainapp import app
from flask import render_template, flash, redirect, url_for
from mainapp.forms import LoginForm
@app.route('/')
@app.route('/index')
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
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)
