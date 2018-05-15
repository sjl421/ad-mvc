import _thread
import socket

from utils import log
from request import Request
from routes import error
from routes.routes_pulic import route_dict as public_routes
from routes.routes_user import route_dict as user_routes


def response_for_path(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {}
    r.update(public_routes())
    r.update(user_routes())
    response = r.get(request.path, error)
    return response(request)


def process_reqeust(connection):
    with connection as con:
        raw_data = b''
        buffer_size = 1024
        while True:
            r = con.recv(buffer_size)
            raw_data += r
            if len(r) < buffer_size:
                break

        raw_data = raw_data.decode()
        log('接收到 raw_data <{}>'.format(raw_data))
        if len(raw_data) > 0:
            request = Request(raw_data)
            log('接收到 request {}'.format(request))

            response = response_for_path(request)
            con.sendall(response)
            log('发送出 response <{}>'.format(response))


def run(host, port):
    """
    启动服务器
    """
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        log('服务器监听启动 http://{}:{}'.format(host, port))

        while True:
            connection, address = s.accept()
            _thread.start_new_thread(process_reqeust, (connection,))


if __name__ == '__main__':
    config = dict(
        host='localhost',
        port=3000,
    )
    run(**config)
