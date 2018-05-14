from . import (
    template,
    html_response,
    redirect,
)

from models.user import User


def register(request):
    form = request.form()
    User.new(form)
    return redirect('/register/view')


def register_view(request):
    t = template('register.html')
    return html_response(t)


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/register/view': register_view,
        '/register': register,
    }
    return d
