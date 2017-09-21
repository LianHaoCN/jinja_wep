#/usr/bin/python
#-*-coding=utf-8-*-
#web.py
'''
'''

# ȫ��ThreadLocal����
ctx = threading.local()

# HTTP������:
class HttpError(Exception):
    pass

# request����:
class Request(object):
    # ����key����value:
    def get(self, key, default=None):
        pass

    # ����key-value��dict:
    def input(self):
        pass

    # ����URL��path:
    @property
    def path_info(self):
        pass

    # ����HTTP Headers:
    @property
    def headers(self):
        pass

    # ����key����Cookie value:
    def cookie(self, name, default=None):
        pass

# response����:
class Response(object):
    # ����header:
    def set_header(self, key, value):
        pass

    # ����Cookie:
    def set_cookie(self, name, value, max_age=None, expires=None, path='/'):
        pass

    # ����status:
    @property
    def status(self):
        pass
    @status.setter
    def status(self, value):
        pass

# ����GET:
def get(path):
    pass

# ����POST:
def post(path):
    pass

# ����ģ��:
def view(path):
    pass

# ����������:
def interceptor(pattern):
    pass

# ����ģ������:
class TemplateEngine(object):
    def __call__(self, path, model):
        pass

# ȱʡʹ��jinja2:
class Jinja2TemplateEngine(TemplateEngine):
    def __init__(self, templ_dir, **kw):
        from jinja2 import Environment, FileSystemLoader
        self._env = Environment(loader=FileSystemLoader(templ_dir), **kw)

    def __call__(self, path, model):
        return self._env.get_template(path).render(**model).encode('utf-8')

        
class WSGIApplication(object):
    def __init__(self, document_root=None, **kw):
        pass

    # ���һ��URL����:
    def add_url(self, func):
        pass

    # ���һ��Interceptor����:
    def add_interceptor(self, func):
        pass

    # ����TemplateEngine:
    @property
    def template_engine(self):
        pass

    @template_engine.setter
    def template_engine(self, engine):
        pass

    # ����WSGI������:
    def get_wsgi_application(self):
        def wsgi(env, start_response):
            pass
        return wsgi

    # ����ģʽ��ֱ������������:
    def run(self, port=9000, host='127.0.0.1'):
        from wsgiref.simple_server import make_server
        server = make_server(host, port, self.get_wsgi_application())
        server.serve_forever()
        
        
wsgi = WSGIApplication()
if __name__ == '__main__':
    wsgi.run()
else:
    application = wsgi.get_wsgi_application()

## ��ҳ:
#@get('/')
#def index():
#    return '<h1>Index page</h1>'
#
## ��������URL:
#@get('/user/:id')
#def show_user(id):
#    user = User.get(id)
#    return 'hello, %s' % user.name
#    
##URL������
#@interceptor('/manage/')
#def check_manage_url(next):
#    if current_user.isAdmin():
#        return next()
#    else:
#        raise seeother('/signin')
#        
##��Ⱦģ��
#@view('index.html')
#@get('/')
#def index():
#    return dict(blogs=get_recent_blogs(), user=get_current_user())
#    
##�ӱ��л�ȡ����
#@get('/test')
#def test():
#    input_data = ctx.request.input()
#    ctx.response.content_type = 'text/plain'
#    ctx.response.set_cookie('name', 'value', expires=3600)
#    return 'result'
#    
##������
#raise seeother('/signin')
#raise notfound()