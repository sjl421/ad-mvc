import json
from urllib.parse import unquote_plus


class Request(object):
    def __init__(self, raw_data):
        self.method = ''
        self.path = ''
        self.headers = {}
        self.cookies = {}
        self.args = {}
        self.body = b''

        self.parse_raw_data(raw_data)

    def __repr__(self):
        classname = self.__class__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def parse_raw_data(self, raw_data):
        header, body = raw_data.split(b'\r\n\r\n', 1)
        # header 都是文本故直接 decode
        self.parse_header(header.decode())
        # body 即可能是文本也可能是图片等二进制数据
        # 故不在此处 decode，必要的时候再执行
        self.body = body

    def parse_header(self, header):
        h, content = header.split('\r\n', 1)
        h = h.split()

        self.method = h[0]
        self.parse_path(h[1])

        content = content.split('\r\n')
        headers = {}
        for c in content:
            k, v = c.split(': ')
            headers[k] = v
        self.headers = headers

        if 'Cookie' in headers:
            cookie = headers['Cookie'].split('; ')
            cookies = {}
            for c in cookie:
                k, v = c.split('=')
                cookies[k] = v
            self.cookies = cookies

    def parse_path(self, path):
        if '?' in path:
            path, params_string = path.split('?', 1)

            params = params_string.split('&')
            args = {}
            for p in params:
                k, v = (unquote_plus(s) for s in p.split('='))
                args[k] = v
            self.args = args

        self.path = unquote_plus(path)

    def form(self):
        body = self.body.decode()

        form = {}
        if '&' in body:
            params = body.split('&')
            for p in params:
                k, v = (unquote_plus(s) for s in p.split('='))
                form[k] = v

        return form

    def json(self):
        body = self.body.decode()
        return json.loads(body)
