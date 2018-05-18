from functools import wraps

from models.note import Note
from . import (
    current_user,
    json_response,
    api_login_required,
    api_error_response,
    api_csrf_required,
)


@api_login_required
def all(request):
    js = Note.all_json()
    return json_response(js)


@api_login_required
@api_csrf_required
def add(request):
    form = request.json()
    u = current_user(request)

    form['user_id'] = u.id
    n = Note.new(form)

    return json_response(n.json())


def admin_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        u = current_user(request)
        if u.is_admin():
            return route_function(request)
        else:
            return api_error_response('需要管理员权限')

    return wrapper


@api_login_required
@admin_required
@api_csrf_required
def delete(request):
    form = request.json()
    note_id = int(form['id'])

    Note.delete(id=note_id)

    m = dict(
        message='删除成功',
    )
    return json_response(m)


def ownership_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        form = request.json()
        note_id = int(form['id'])

        n = Note.find_by(id=note_id)
        u = current_user(request)

        if u.id == n.user_id:
            return route_function(request)
        else:
            return api_error_response('只有所属用户才能操作')

    return wrapper


@api_login_required
@ownership_required
@api_csrf_required
def update(request):
    form = request.json()
    n = Note.update(form)
    return json_response(n.json())


def route_dict():
    d = {
        '/api/note/all': all,
        '/api/note/add': add,
        '/api/note/delete': delete,
        '/api/note/update': update,
    }
    return d
