#!/usr/bin/python
#-*-coding=utf-8-*-
#db.py
'''
数据库模块
用法：
import db
db.create_engine(user, password, database, host, port)
支持的sql语句，可直接使用：
    db.select('...')
    db.update('...')

with db.connection():
    sql语句
with db.transactions():
    sql语句
'''

import mysql.connector, threading, functools

#数据库引擎对象
class _Engine(object):
    def __init__(self, connect):
        self._connect = connect
    def connect(self):
        return self._connect()

engine = None

#数据库连接对象
class _LasyConnection():
    def __init__(self):
        self.connect = None
        self.cur = None
    def cleanup(self):
        self.cur.close()
        self.connect.close()
        self.connect.disconnect()
        self.connect = None
        self.cur = None
    def cursor(self):
        global engine
        self.connect = engine.connect()
        self.cur = self.connect.cursor(dictionary=True)
        return self.cur
    def commit(self):
        self.connect.commit()
    def rollback(self):
        self.connect.rollback()

#持有数据库连接的上下文对象
class _DBCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transactions = 0
    def is_init(self):
        return not self.connection is None
    def init(self):
        self.connection = _LasyConnection()
        self.transactions = 0
    def cleanup(self):
        self.connection.cleanup()
        self.connection = None
    def cursor(self):
        return self.connection.cursor()

_db_ctx = _DBCtx()

#数据库连接，自动获取和释放
class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self
    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()

def connection():
    return _ConnectionCtx()

def with_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        with connection():
            return func(*args, **kw)
    return wrapper

@with_connection
def select(sql):
    global _db_ctx
    cursor = _db_ctx.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

@with_connection
def update(sql, *args):
    global _db_ctx
    cursor = _db_ctx.cursor()
    cursor.execute(sql, list(args))
    affectrows = cursor.rowcount
    _db_ctx.connection.commit()
    return str(affectrows) + ' rows affect (update or insert or delete)'
    
    
class _TransactionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions = _db_ctx.transactions + 1
        return self
    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions = _db_ctx.transactions - 1
        try:
            if _db_ctx.transactions==0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()
    def commit(self):
        global _db_ctx
        try:
            _db_ctx.connection.commit()
        except:
            _db_ctx.connection.rollback()
            raise
    def rollback(self):
        global _db_ctx
        _db_ctx.connection.rollback()
    
def transaction():
    return _TransactionCtx()
    
    
def create_engine(user, password, database, host, port):
    params = {'host':host, 'port':port, 'database':database, 'user':user, 'password':password}
    global engine
    engine = _Engine(lambda:mysql.connector.connect(**params))

if __name__ == '__main__':
    create_engine(user='root', password='TZTJ-VCeIoCM1CG1dWe3', database='test', host='127.0.0.1', port='3306')
    #print select('select * from user')
    #with connection():
    #    print update('update user t set t.name=%s where t.id=%s','mark',2)
    #    print select('select * from user')
    #with transaction():
    #    print select('select * from user')
    #    print update('update user t set t.name=%s where t.id=%s','jack',2)
    #print select('select * from user')
    