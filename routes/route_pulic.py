from . import(
    template,
    html_response,
)


def index(request):
    t = template('index.html')
    return html_response(t)


def static(request):
    """
    静态资源的处理函数, 读取文件并生成响应返回
    """
    filename = request.args['file']
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\n\r\n'
        img = header + f.read()
        return img


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/': index,
        '/static': static,
    }
    return d
