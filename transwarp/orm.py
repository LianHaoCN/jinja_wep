#!/usr/bin/python
#-*-coding=utf-8-*-
#orm.py
'''
ORM模块: 实例可以直接对库表进行增删改查
用法：
import orm, db
db.create_engine(user, password, database, host, port)
class User(Model):
    __table__ = 'user'
    id = IntegerField('id', primary_key=True)
    name = StringField('name')
    ...
实例用法
user = User(id=11, name='Michael')
user.insert()                                           #增加
User.get('12')                                          #按键值条件查询，获取第一条记录，返回实例
User.find_first('where email="?"', 'test@example.com')  #条件查询，按键值排序后，返回第一条记录
User.find_all()                                         #按键值排序后，查所有记录
User.find_by('name', 'Michael', 'id')                   #条件查询，按指定列排序后，查所有记录
User.count_all()                                        #单表记录总数
User.count_by('name', 'Michael')                        #条件查询到的记录数
user.update()                                           #改
user.delete()                                           #删
'''

import db, time

class Field(object):
    def __init__(self, primary_key, default, updatable, ddl):
        self.name = ''
        self.primary_key = primary_key
        self.default = default
        self.updatable = updatable
        self.ddl = ddl
               
class StringField(Field):
    def __init__(self, primary_key=False, default='', updatable=True, ddl='varchar(20)'):
        super(StringField, self).__init__(primary_key, default, updatable, ddl)
        
class BooleanField(Field):
    def __init__(self, primary_key=False, default=0, updatable=True, ddl='bool'):
        super(BooleanField, self).__init__(primary_key, default, updatable, ddl)
        
class FloatField(Field):
    def __init__(self, primary_key=False, default=0.0, updatable=True, ddl='real'):
        super(FloatField, self).__init__(primary_key, default, updatable, ddl)
        
class TextField(Field):
    def __init__(self, primary_key=False, default='', updatable=True, ddl='mediumtext'):
        super(TextField, self).__init__(primary_key, default, updatable, ddl)

        
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        unupdatable = []
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                v.name = k
                #print v.updatable, v.name, v
                if v.updatable is False:
                    unupdatable.append(v.name)
                if v.primary_key:
                    primary_key = v
                mappings[k] = v
        #print unupdatable
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__primary_key__'] = primary_key
        attrs['__unupdatable__'] = unupdatable
        #print cls,'\n', name,'\n', bases,'\n', attrs,'\n'
        return type.__new__(cls, name, bases, attrs)

class Model(dict):
    __metaclass__ = ModelMetaclass
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value
    @classmethod
    def get(cls, pk):
        d = db.select_one('select * from %s where %s="?"' % (cls.__table__, cls.__primary_key__.name), pk)
        return cls(**d) if d else None
    @classmethod
    def find_first(cls, col, pk):
        d = db.select_one('select * from %s %s order by %s' % (cls.__table__, col, cls.__primary_key__.name), pk)
        return cls(**d) if d else None
    @classmethod
    def find_all(cls):
        d = db.select('select * from %s order by "?"' % cls.__table__, cls.__primary_key__.name)
        return [cls(**instance) for instance in d] if d else None
    @classmethod
    def find_by(cls, col, pk, order_col):
        d = db.select('select * from %s where %s="?" order by %s' % (cls.__table__, col, order_col), pk)
        return [cls(**instance) for instance in d] if d else None
    @classmethod
    def count_all(cls):
        return db.select_one('select count(*) from ?', cls.__table__).values()[0]
    @classmethod
    def count_by(cls, col, pk):
        d = db.select_one('select count(*) from %s where %s="?"' % (cls.__table__, col), pk)
        return d.values()[0]
        
    def insert(self):
        params = {}
        for k, v in self.__mappings__.iteritems():
            #print k, v
            try:
                params[v.name] = getattr(self, k)
            except AttributeError:
                if callable(v.default):
                    if v.default==db.next_id:
                        self[v.name] = params[v.name] = v.default(self.__table__)
                    else:
                        self[v.name] = params[v.name] = v.default()
                else:
                    self[v.name] = params[v.name] = v.default
        db.insert(self.__table__, params)
        return self
        
    def delete(self):
        pk = getattr(self, self.__primary_key__.name)
        db.delete(self.__table__, self.__primary_key__.name, pk)

    def update(self):
        pk = getattr(self, self.__primary_key__.name)
        old = self.get(str(pk))
        if old:
            if old<>self:
                params = {}
                for k, v in self.__mappings__.iteritems():
                    if v.name<>self.__primary_key__.name:
                        params[v.name] = getattr(self, k)
                for i in self.__unupdatable__:
                    params.pop(i)
                #print params
                sql = 'update %s set %s where %s="?"' % (self.__table__, ','.join('%s="%s"' %(i,params[i]) for i in params), self.__primary_key__.name)
                db.update(sql, str(pk))
            else:
                print 'warnning: database has the same record'
        else:
            print 'Error: databases has no record, please use insert method'


if __name__=='__main__':
    db.create_engine(user='root', password='TZTJ-VCeIoCM1CG1dWe3', database='test', host='127.0.0.1', port='3306')
    class User(Model):
        __table__ = 'user'
        id = IntegerField('id', primary_key=True)
        name = StringField('name')
    user = User(id=13, name='jeff')
    user.insert()
    print User.get('12')
    print User.find_first('name', 'Michael')
    print User.find_all('name', 'Michael')
    print User.find_by('name', 'Michael', 'id')
    print User.count_all()
    print User.count_by('name', 'Michael')
    user = User(id=13, name='Michael')
    user.update()
    user = User(id=2, name='jack')
    user.delete()
    