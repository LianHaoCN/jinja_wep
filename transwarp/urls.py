#!/usr/bin/python
#-*-coding=utf-8-*-
#urls.py
'''
'''

from web import get, view
from model import User, Blog, Comment

@view('test_users.html')
@get('/')
def test_users():
    users = User.find_all()
    return dict(users=users)