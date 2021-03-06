#/usr/bin/python
#-*-coding=utf-8-*-
#web.py
'''
'''

import threading

# 全局ThreadLocal对象：
ctx = threading.local()

# HTTP错误类:
class HttpError(Exception):
    pass

# request对象:
class Request(object):
    # 根据key返回value:
    def get(self, key, default=None):
        pass

    # 返回key-value的dict:
    def input(self):
        pass

    # 返回URL的path:
    @property
    def path_info(self):
        pass

    # 返回HTTP Headers:
    @property
    def headers(self):
        pass

    # 根据key返回Cookie value:
    def cookie(self, name, default=None):
        pass

# response对象:
class Response(object):
    # 设置header:
    def set_header(self, key, value):
        pass

    # 设置Cookie:
    def set_cookie(self, name, value, max_age=None, expires=None, path='/'):
        pass

    # 设置status:
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        self._status = value

# 定义GET:
def get(path):
    pass

# 定义POST:
def post(path):
    pass

# 定义模板:
def view(path):
    pass

# 定义拦截器:
def interceptor(pattern):
    pass

# 定义模板引擎:
class TemplateEngine(object):
    def __call__(self, path, model):
        pass

# 缺省使用jinja2:
class Jinja2TemplateEngine(TemplateEngine):
    def __init__(self, templ_dir, **kw):
        from jinja2 import Environment, FileSystemLoader
        self._env = Environment(loader=FileSystemLoader(templ_dir), **kw)

    def __call__(self, path, model):
        return self._env.get_template(path).render(**model).encode('utf-8')
        
        
class WSGIApplication(object):
    def __init__(self, document_root=None, **kw):
        pass

    # 添加一个URL定义:
    def add_url(self, func):
        pass

    # 添加一个Interceptor定义:
    def add_interceptor(self, func):
        pass

    # 设置TemplateEngine:
    @property
    def template_engine(self):
        return self._engine

    @template_engine.setter
    def template_engine(self, engine):
        self._engine = engine

    # 返回WSGI处理函数:
    def get_wsgi_application(self):
        def wsgi(env, start_response):
            self.template_engine = Jinja2TemplateEngine('../www/templates')
            start_response('200 OK', [('Content-Type', 'text/html')])
            return self.template_engine('home.html', {})#{'the':'variables', 'go':'here'})
        return wsgi

    # 开发模式下直接启动服务器:
    def run(self, port=9000, host='0.0.0.0'):
        from wsgiref.simple_server import make_server
        server = make_server(host, port, self.get_wsgi_application())
        server.serve_forever()
        

## 首页:
#@get('/')
#def index():
#    return '<h1>Index page</h1>'
#
## 带参数的URL:
#@get('/user/:id')
#def show_user(id):
#    user = User.get(id)
#    return 'hello, %s' % user.name
#    
##URL拦截器
#@interceptor('/manage/')
#def check_manage_url(next):
#    if current_user.isAdmin():
#        return next()
#    else:
#        raise seeother('/signin')
#        
##渲染模板
#@view('index.html')
#@get('/')
#def index():
#    return dict(blogs=get_recent_blogs(), user=get_current_user())
#    
##从表单中获取数据
#@get('/test')
#def test():
#    input_data = ctx.request.input()
#    ctx.response.content_type = 'text/plain'
#    ctx.response.set_cookie('name', 'value', expires=3600)
#    return 'result'
#    
##错误处理
#raise seeother('/signin')
#raise notfound()


wsgi = WSGIApplication()
if __name__ == '__main__':
    wsgi.run()
else:
    application = wsgi.get_wsgi_application()
    