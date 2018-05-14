import uuid

from models.session import Session
from . import (
    current_user,
    html_response,
    redirect,
)

from template import Template
from models.user import User


def register_view(request):
    us = User.all()
    t = Template.render('register.html', users=us)
    return html_response(t)


def register(request):
    form = request.form()
    User.new(form)
    return redirect('/register/view')


def login_view(request):
    u = current_user(request)
    result = request.args.get('result', '')
    t = Template.render('login.html', username=u.username, result=result)
    return html_response(t)


def login(request):
    form = request.form()
    u = User.find_by(**form)

    if u is not None:
        session_id = str(uuid.uuid4())
        form = dict(
            session_id=session_id,
            user_id=u.id,
        )
        Session.new(form)

        headers = {
            'Set-Cookie': 'session_id={}'.format(session_id),
        }
        result = '登陆成功'

        return redirect('/login/view?result={}'.format(result), headers)
    else:
        result = '登录失败'
        return redirect('/login/view?result={}'.format(result))


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/register/view': register_view,
        '/register': register,
        '/login/view': login_view,
        '/login': login,
    }
    return d
