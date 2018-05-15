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

    return json_response(n.json())


def delete(request):
    form = request.json()
    note_id = int(form['id'])

    Note.delete(id=note_id)

    m = dict(
        message='删除成功',
    )
    return json_response(m)


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
