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


def run(self, server_class=HTTPServer, handler_class=HttpHandler) -> None:
    logging.debug('Server Wake up!')
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


serverthread = Thread(target=run_server)
clientthread = Thread(target=run)
