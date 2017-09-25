#!/usr/bin/python
#-*-coding=utf-8-*-
#wsgiapp.py

import logging;
logging.basicConfig(level=logging.INFO)
import os

import db
from web import WSGIApplication, Jinja2TemplateEngine
from config import configs

#��ʼ�����ݿ�
db.create_engine(**configs['db'])

##����һ��WSGIApplication
workpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print workpath, os.path.join(workpath, 'www', 'templates')
wsgi = WSGIApplication(workpath)
#��ʼ��jinja2ģ������
template_engine = Jinja2TemplateEngine(os.path.join(workpath, 'www', 'templates'))
wsgi.template_engine = template_engine

##���ش���@get/@post��URL������
import urls
#print urls
wsgi.add_module(urls)
#
##��9000�˿����������ز��Է�����
if __name__ == '__main__':
    print urls.test_users()
    wsgi.run(9000)