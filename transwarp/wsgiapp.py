#!/usr/bin/python
#-*-coding=utf-8-*-
#wsgiapp.py

import logging;
logging.basicConfig(level=logging.INFO)
import os

import db
from web import WSGIApplication, Jinja2TemplateEngine
from config import configs

#初始化数据库
db.create_engine(**configs['db'])

##创建一个WSGIApplication
workpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print workpath, os.path.join(workpath, 'www', 'templates')
wsgi = WSGIApplication(workpath)
#初始化jinja2模板引擎
template_engine = Jinja2TemplateEngine(os.path.join(workpath, 'www', 'templates'))
wsgi.template_engine = template_engine

##加载带有@get/@post的URL处理函数
import urls
#print urls
wsgi.add_module(urls)
#
##在9000端口上启动本地测试服务器
if __name__ == '__main__':
    print urls.test_users()
    wsgi.run(9000)