import _thread
import socket

from utils import log
from request import Reqeust


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
            request = Reqeust(raw_data)
            log('接收到 request {}'.format(request))

            con.sendall(b'recived!')


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
        host="127.0.0.1",
        port=3000,
    )
    run(**config)