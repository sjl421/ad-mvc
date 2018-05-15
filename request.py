import json
from urllib.parse import unquote_plus


class Reqeust(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.method = ''
        self.path = ''
        self.headers = {}
        self.cookies = {}
        self.args = {}
        self.body = ''

        self.setup()

    def __repr__(self):
        classname = self.__class__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def setup(self):
        header, body = self.raw_data.split('\r\n\r\n', 1)
        self.parse_header(header)
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
        path = unquote_plus(path)

        if '?' in path:
            path, params_string = path.split('?', 1)
            self.path = path

            params = params_string.split('&')
            args = {}
            for p in params:
                k, v = p.split('=')
                args[k] = v
            self.args = args
        else:
            self.path = path

    def form(self):
        body = unquote_plus(self.body)

        form = {}
        if '&' in body:
            params = body.split('&')
            for p in params:
                k, v = p.split('=')
                form[k] = v

        return form

    def json(self):
        body = unquote_plus(self.body)
        return json.loads(body)
