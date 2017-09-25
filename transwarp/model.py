#!/usr/bin/python
#-*-coding=utf-8-*-
#model.py
'''
model模块：
import db
from models import User, Blog, Comment
db.create_engine(user, password, database, host, port)
u = User(name='Test', email='test@example.com', password='123456', image='about:blank')
b = Blog(...)
c = Comment(...)
可以调用orm模块的方法
insert()                                            #增加
get('12')                                           #按键值条件查询，获取第一条记录，返回实例
find_first('where email="?"', 'test@example.com')   #条件查询，按键值排序后，返回第一条记录
find_all()                                          #按键值排序后，查所有记录
find_by('name', 'Michael', 'id')                    #条件查询，按指定列排序后，查所有记录
count_all()                                         #单表记录总数
count_by('name', 'Michael')                         #条件查询到的记录数
update()                                            #改
delete()                                            #删
'''

import time, uuid
from db import next_id, create_engine
from orm import Model, StringField, BooleanField, FloatField, TextField

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
    create_engine(user='root', password='TZTJ-VCeIoCM1CG1dWe3', database='awesome', host='127.0.0.1', port='3306')
    u = User(name='Test', email='test@example.com', password='123456', image='about:blank')
    u.insert()
    print 'new user:', u.id
    
    #u = User.find_first('where email="?"', 'test@example.com')
    #u.password = '111111'
    #u.update()
    u1 = User.find_first('where email="?"', 'test@example.com')
    print 'find user\'s name:', u1.name
    u1.delete()
    u2 = User.find_first('where email="?"', 'test@example.com')
    print 'find user:', u2