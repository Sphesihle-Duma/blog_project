#!/usr/bin/env python3
'''
   Models module that define the structure of the database
'''
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from mainapp import db

class User(db.Model):
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

    def __repr__(self):
        '''
           String represetation
        '''
        return '<User {}>'.format(self.username)

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
