#!/usr/bin/env python3
'''
   Models module that define the structure of the database
'''
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from mainapp import db, login

class User(db.Model, UserMixin):
    '''
      User model for user table in the database
    '''
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        '''
           String represetation
        '''
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """
           setting a password for a user
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''
           verifying the user's password
        '''
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        ''' creating images for users
        '''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

@login.user_loader
def load_user(id):
    ''' grabbing the unique id for the user in the session,
    return the logged in user
    '''
    return db.session.get(User, int(id))



class Post(db.Model):
    '''
       Post model for post table in the database.
    '''
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
            index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[User] = so.mapped_column(sa.ForeignKey(User.id),
                                                index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')
    
    def __repr__(self):
        '''
           string represetation of the posts
        '''
        return '<Post> {}'.format(self.body)
