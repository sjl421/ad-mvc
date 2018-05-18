from template import Template
from utils import log
from . import (
    html_response,
    current_user,
    error_response,
)


def index(request):
    u = current_user(request)
    t = Template.render('index.html', username=u.username)
    return html_response(t)


def static(request):
    """
    静态资源的处理函数, 读取文件并生成响应返回
    """
    filename = request.args['file']

    # 出于安全考虑，避免访问到 static 目录之外
    if '..' in filename:
        r = error_response(request, 403)
        log(403, r)
        return r

    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        src = header + f.read()
        return src


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/': index,
        '/static': static,
    }
    return d
