import _thread
import socket

from utils import log


def process_reqeust(connection):
    with connection as con:
        request = b''
        buffer_size = 1024
        while True:
            r = con.recv(buffer_size)
            request += r
            if len(r) < buffer_size:
                break
        log('接收到 request <{}>'.format(request.decode()))

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
