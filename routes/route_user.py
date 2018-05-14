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
    result = request.args.get('result', '')
    t = Template.render('register.html', result=result)
    return html_response(t)


def register(request):
    form = request.form()
    result = User.register(form)
    return redirect('/user/register/view?result={}'.format(result))


def login_view(request):
    u = current_user(request)
    result = request.args.get('result', '')
    t = Template.render('login.html', username=u.username, result=result)
    return html_response(t)


def login(request):
    form = request.form()
    u, result = User.login(form)

    if u is not None:
        session_id = str(uuid.uuid4())
        form = dict(
            session_id=session_id,
            user_id=u.id,
        )
        Session.new(form)

        headers = {
            'Set-Cookie': 'session_id={}; path=/'.format(session_id),
        }

        return redirect('/user/login/view?result={}'.format(result), headers)
    else:
        return redirect('/user/login/view?result={}'.format(result))


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/user/register/view': register_view,
        '/user/register': register,
        '/user/login/view': login_view,
        '/user/login': login,
    }
    return d
