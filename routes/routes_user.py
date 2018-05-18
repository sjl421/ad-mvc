from functools import wraps

from models.session import Session
from models.csrf_token import CsrfToken
from . import (
    current_user,
    html_response,
    redirect,
    login_required,
    csrf_required,
)

from template import Template
from models.user import User


def register_view(request):
    result = request.args.get('result', '')
    u = current_user(request)
    token = CsrfToken.new()

    t = Template.render(
        '/user/register.html',
        username=u.username,
        result=result,
        csrf_token=token
    )
    return html_response(t)


@csrf_required
def register(request):
    form = request.form()
    result = User.register(form)
    return redirect('/user/register/view?result={}'.format(result))


def login_view(request):
    result = request.args.get('result', '')
    u = current_user(request)
    t = Template.render('/user/login.html', username=u.username, result=result)
    return html_response(t)


def login(request):
    form = request.form()
    u, result = User.login(form)

    if u is not None:
        session = Session.new(u)
        headers = {
            'Set-Cookie': 'session={}; HttpOnly; path=/'.format(session),
        }
        return redirect('/user/login/view?result={}'.format(result), headers)
    else:
        return redirect('/user/login/view?result={}'.format(result))


def same_user_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        args = request.args
        if 'id' in args:
            user_id = int(args['id'])
        else:
            form = request.form()
            user_id = int(form['id'])
        u = current_user(request)

        if u.id == user_id:
            return route_function(request)
        else:
            return redirect('/user/admin?result={}'.format('权限不足'))

    return wrapper


def admin_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        u = current_user(request)
        if u.is_admin():
            return route_function(request)
        else:
            return redirect('/user/admin?result={}'.format('权限不足'))

    return wrapper


@login_required
def admin(request):
    result = request.args.get('result', '')

    us = User.all()
    u = current_user(request)

    t = Template.render('/user/admin.html', username=u.username, users=us, result=result)
    return html_response(t)


@login_required
@same_user_required
def edit(request):
    user_id = int(request.args['id'])
    u = User.find_by(id=user_id)

    cu = current_user(request)
    username = cu.username

    t = Template.render('/user/edit.html', username=username, user=u)
    return html_response(t)


@login_required
@same_user_required
def update(request):
    form = request.form()
    result = User.update(form)
    return redirect('/user/admin?result={}'.format(result))


@login_required
@admin_required
def delete(request):
    user_id = int(request.args['id'])
    User.delete(user_id)
    return redirect('/user/admin?result={}'.format('删除成功'))


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
        '/user/admin': admin,
        '/user/delete': delete,
        '/user/edit': edit,
        '/user/update': update,
    }
    return d
