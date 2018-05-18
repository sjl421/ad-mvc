from functools import wraps

from models.csrf_token import CsrfToken
from models.session import Session
from models.user import User


def current_user(request):
    session = request.cookies.get('session')
    u = Session.find_user(session)
    return u if u is not None else User.guest()


def formatted_header(headers, code=200, phrase='OK'):
    header = 'HTTP/1.1 {} {}\r\n'.format(code, phrase)
    header += ''.join(
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    )
    return header


def html_response(body, headers=None):
    h = {
        'Content-Type': 'text/html',
    }

    if headers is None:
        headers = h
    else:
        headers.update(h)

    header = formatted_header(headers)
    r = header + '\r\n' + body

    return r.encode()


def redirect(url, headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    h = {
        'Location': url,
    }

    if headers is None:
        headers = h
    else:
        headers.update(h)

    r = formatted_header(headers, 302, 'REDIRECT') + '\r\n'
    return r.encode()


def error_response(request, code=404):
    """
    根据 code 返回不同的错误响应
    """
    e = {
        401: b'HTTP/1.1 401 Unauthorized\r\n\r\n<h1>Unauthorized</h1><a href="/">Home</a>',
        403: b'HTTP/1.1 403 Forbidden\r\n\r\n<h1>Forbidden</h1><a href="/">Home</a>',
        404: b'HTTP/1.1 404 Not Found\r\n\r\n<h1>Not Found</h1><a href="/" >Home</a>',
    }
    return e.get(code, b'')


def login_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        u = current_user(request)
        if u.is_guest():
            return redirect('/user/login/view')
        else:
            return route_function(request)

    return wrapper


def csrf_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        token = request.query['csrf_token']

        if CsrfToken.valid(token):
            CsrfToken.delete(token)
            return route_function(request)
        else:
            return error_response(request, 401)

    return wrapper
