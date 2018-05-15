from . import (
    current_user,
    html_response,
)
from template import Template


def index(request):
    u = current_user(request)
    t = Template.render('/note/index.html', username=u.username)
    return html_response(t)


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/note/index': index,
    }
    return d