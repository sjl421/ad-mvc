def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


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


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')
