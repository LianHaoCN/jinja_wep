#!/usr/bin/python
#-*-coding=utf-8-*-
#wsgiapp.py

import logging;
logging.basicConfig(level=logging.INFO)
import os

import transwarp.db
from transwarp.web import WSGIApplication, Jinja2TemplateEngine
from transwarp.config import configs

#��ʼ�����ݿ�
db.create_engine(**configs['db'])

##����һ��WSGIApplication
print os.path.dirname(os.path.abspath(__file__))
print os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
wsgi = WSGIApplication(os.path.dirname(os.path.abspath(__file__)))
##��ʼ��jinja2ģ������
template_engine = Jinja2TemplateEngine(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
wsgi.template_engine = template_engine
#
##���ش���@get/@post��URL������
#import urls
#wsgi.add_module(urls)
#
##��9000�˿����������ز��Է�����
#if __name__ == '__main__':
#    wsgi.run(9000)