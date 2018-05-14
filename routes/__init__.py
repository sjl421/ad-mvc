def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


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


def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    headers = {
        'Location': url,
    }
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
