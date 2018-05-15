from models.note import Note
from . import (
    current_user,
    json_response,
)


def all(request):
    js = Note.all_json()
    return json_response(js)


def add(request):
    form = request.json()
    u = current_user(request)
    form['user_id'] = u.id

    n = Note.new(form)

    m = dict(
        message='添加成功',
        note=n.json(),
    )
    return json_response(m)


def delete(request):
    form = request.json()
    note_id = form['id']

    Note.delete(id=note_id)

    m = dict(
        message='删除成功',
    )
    return json_response(m)


def update(request):
    form = request.json()
    n = Note.update(form)

    m = dict(
        message='修改成功',
        note=n.json(),
    )
    return json_response(m)


def route_dict():
    d = {
        '/api/note/all': all,
        '/api/note/add': add,
        '/api/note/delete': delete,
        '/api/note/update': update,
    }
    return d
