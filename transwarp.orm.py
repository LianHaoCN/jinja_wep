#-*-coding=utf-8-*-

import db

class Field(object):
    def __init__(self, name, column_type, primary_key):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)
    def is_primary_key(self):
        return self.name if self.primary_key else None 
        
class StringField(Field):
    def __init__(self, name, primary_key=False):
        super(StringField, self).__init__(name, 'varchar(100)', primary_key)
        
class IntegerField(Field):
    def __init__(self, name, primary_key=False):
        super(IntegerField, self).__init__(name, 'bigint', primary_key)

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        print cls,'\n', name,'\n', bases,'\n', attrs,'\n'
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print('Found mapping: %s==>%s' % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__table__'] = name
        attrs['__mappings__'] = mappings
        return type.__new__(cls, name, bases, attrs)
        #mapping = cls.__class__.__name__ #读取cls的Field字段
        #primary_key = cls.name if cls.is_primary_key() #查找primary_key字段
        #__table__ = cls.__class__ #读取cls的__table__字段
        ##给cls增加一些字段
        #attrs['__mapping__'] = mapping
        #attrs['__primary_key__'] = __primary_key__
        #attrs['__table__'] = __table__
        #return type.__new__(cls, name, bases, attrs)

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
        #d = db.select_one('select * from %s where %s=?' % (cls.__table__, cls.__primary_key__.name), pk)
        d = db.select('select * from %s where %s=?' % (cls.__table__, cls.__primary_key__.name), pk)
        return cls(**d) if d else None
#    def insert(self):
#        params = {}
#        for k, v in self.__mappings__.iteritems():
#            params[v.name] = getattr(self, k)
#        db.insert(self.__table__, **params)
#    return self
    #def find_first()
    #def find_all()
    #def find_by()
    #def count_all()
    #def count_by()
    #def update()
    #def delete()


if __name__=='__main__':
    class User(Model):
        __table__ = 'user'
        id = IntegerField('id', primary_key=True)
        name = StringField('name')
    user = User(id=123, name='Michael')
    print user.id, user.name
    db.create_engine(user='root', password='TZTJ-VCeIoCM1CG1dWe3', database='test', host='127.0.0.1', port='3306')
    user = User.get('1')
    