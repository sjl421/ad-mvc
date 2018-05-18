from models.csrf_token import CsrfToken
from template import Template
from . import (
    current_user,
    html_response,
    login_required,
)


@login_required
def index(request):
    u = current_user(request)
    token = CsrfToken.new()
    t = Template.render(
        '/note/index.html',
        username=u.username,
        csrf_token=token,
    )
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
