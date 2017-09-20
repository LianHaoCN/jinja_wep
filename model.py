#!/usr/bin/python
#-*-coding=utf-8-*-
#model.py
'''
modelģ�飺
'''

import time, uuid
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField

class User(Model):
    __table__ = 'users'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(updatable=False, ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(updatable=False, default=time.time)
    
class Blog(Model):
    __table__ = 'blogs'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(updatable=False, default=time.time)
    
class Comment(Model):
    __table__ = 'comments'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(updatable=False, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(updatable=False, default=time.time)
    
if __name__ == '__main__':
    from transwarp import db
    from models import User, Blog, Comment
    db.create_engine(user='root', password='TZTJ-VCeIoCM1CG1dWe3', database='awesome', host='127.0.0.1', port='3306')
    u = User(name='Test', email='test@example.com', password='123456', image='about:blank')
    u.insert()
    print 'new user id:', u.id
    u1 = User.find_first('where email=?', 'test@example.com')
    print 'find user\'s name:', u1.name
    u1.delete()
    u2 = User.find_first('where email=?', 'test@example.com')
    print 'find user:', u2