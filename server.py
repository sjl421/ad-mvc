import _thread
import argparse
import socket

from request import Request
from routes import error_response
from routes.api.note import route_dict as note_api
from routes.note import route_dict as note_routes
from routes.pulic import route_dict as public_routes
from routes.user import route_dict as user_routes
from utils import log


def response_for_request(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {}
    r.update(public_routes())
    r.update(user_routes())
    r.update(note_routes())
    r.update(note_api())

    route_function = r.get(request.path, error_response)
    response = route_function(request)
    return response


def receive_all(connection):
    buffer = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        buffer += r
        if len(r) < buffer_size:
            break
    return buffer


def process_request(connection):
    with connection as con:
        raw_data = receive_all(connection)
        log('接收到 raw_data <{}>'.format(raw_data))

        # chrome 浏览器可能会发空请求
        if len(raw_data) > 0:
            request = Request(raw_data)
            log('接收到 request {}'.format(request))

            # 浏览器可能会将 header 和 body 分开发送
            # 此时，需继续接收 body
            if request.uncompleted():
                raw_data += receive_all(connection)
                request = Request(raw_data)
                log('完整接收到 request {}'.format(request))

            response = response_for_request(request)
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
            _thread.start_new_thread(process_request, (connection,))


def command_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default='8000')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = command_args()
    config = dict(
        host=args.host,
        port=args.port,
    )
    run(**config)
