from models.csrf_token import CsrfToken
from . import (
    current_user,
    html_response,
    login_required,
    cookie_headers,
)
from template import Template


@login_required
def index(request):
    u = current_user(request)

    token = CsrfToken.new()
    headers = cookie_headers('csrf_token', token)

    t = Template.render('/note/index.html', username=u.username)
    return html_response(t, headers)


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
