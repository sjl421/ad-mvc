from models.session import Session
from models.user import User


def current_user(request):
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            return u if u is not None else User.guest()
    else:
        return User.guest()


def response_with_headers(headers, code=200, phrase='OK'):
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

    header = response_with_headers(headers)
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

    r = response_with_headers(headers, 302, 'REDIRECT') + '\r\n'
    return r.encode()


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')
