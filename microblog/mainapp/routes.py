#!/usr/bin/env python3
'''
   Module for handlers
   it imports app which is a member of 
   the package.
   creates supported routes
'''
from mainapp import app, db
from flask import render_template, flash, redirect, url_for, request
from mainapp.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from datetime import datetime, timezone
from urllib.parse import urlsplit
from mainapp.models import User


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
@app.route('/')
@app.route('/index')
@login_required
def index():
    '''
       view function for home page
    '''
    
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
    return render_template('index.html', title='Home', posts=posts)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
       Registering user to the app
    '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    '''
       A view function for user profiles.
    '''
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}
            ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    '''
       view function for editing user profile
    '''
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data - current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
