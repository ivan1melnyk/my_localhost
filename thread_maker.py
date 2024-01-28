from threading import Thread
from http.server import HTTPServer
from server import run_server
from client import HttpHandler
import logging

UDP_IP = '127.0.0.1'
UDP_PORT = 5000

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class ServerThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        run_server(UDP_IP, UDP_PORT)


class ClientThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self, server_class=HTTPServer, handler_class=HttpHandler) -> None:
        logging.debug('Server Wake up!')
        logging.debug(f"args: {self.args}")
        server_address = ('', 3000)
        http = server_class(server_address, handler_class)
        try:
            http.serve_forever()
        except KeyboardInterrupt:
            http.server_close()
