#!/usr/bin/python
#-*-coding=utf-8-*-
#db.py
'''
���ݿ�ģ��
�÷���
import db
db.create_engine(user, password, database, host, port)
֧����ɾ�Ĳ��sql��䣬��ֱ��ʹ�ã�
    db.select('...')
    db.update('...')
    db.delete('...')
    db.insert('...')
    db.select_one('...')
    db.next_id('...')

with db.connection():
    sql���
with db.transactions():
    sql���
'''

import mysql.connector, threading, functools

#���ݿ��������
class _Engine(object):
    def __init__(self, connect):
        self._connect = connect
    def connect(self):
        return self._connect()

engine = None

#���ݿ����Ӷ���
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

#�������ݿ����ӵ������Ķ���
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

#���ݿ����ӣ��Զ���ȡ���ͷ�
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
def next_id(tb):
    global _db_ctx
    sql = 'select max(id)+1 from %s' % tb
    cursor = _db_ctx.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    return 1 if data.values()[0] is None else data.values()[0]

@with_connection
def insert(tb, params):
    global _db_ctx
    #print params
    sql = 'insert into %s (%s) values ("%s")' % (tb, ','.join([i for i in params]), '","'.join([str(params[i]) for i in params]))
    cursor = _db_ctx.cursor()
    cursor.execute(sql)
    affectrows = cursor.rowcount
    _db_ctx.connection.commit()
    print str(affectrows) + ' rows have been insert'
    
@with_connection
def delete(tb, pk, key):
    global _db_ctx
    sql = 'delete from %s where %s="%s"' % (tb, pk, key)
    cursor = _db_ctx.cursor()
    cursor.execute(sql)
    affectrows = cursor.rowcount
    _db_ctx.connection.commit()
    print str(affectrows) + ' rows have been deleted'
    
@with_connection
def select(sql, key):
    global _db_ctx
    sql = sql.replace('?', key)
    cursor = _db_ctx.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data
    
def select_one(sql, key):
    data = select(sql, key)
    return data[0] if data else None

@with_connection
def update(sql, key):
    global _db_ctx
    sql = sql.replace('?', key)
    cursor = _db_ctx.cursor()
    cursor.execute(sql)
    affectrows = cursor.rowcount
    _db_ctx.connection.commit()
    print str(affectrows) + ' rows have been updated'
    
    
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
    #    update('update user t set t.name=%s where t.id=%s','jack',2)
    #print select('select * from user')
    