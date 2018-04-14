import multiprocessing
import os
import socket

from constants import REQUEST_QUEUE_SIZE, BUFFER_SIZE
from request import RequestHandler, Request


class IterativeServer(object):
    def __init__(self, host, port, document_root, logger=None):
        self.socket = None
        self.host = host
        self.port = port
        self.document_root = document_root
        self.logger = logger

    def create_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(REQUEST_QUEUE_SIZE)
        except socket.error as e:
            raise RuntimeError(e)

    def serve_forever(self):
        self.create_socket()
        while True:
            try:
                connection, address = self.socket.accept()
                self.logger.info("Connection accepted. Process: {} PID: {}".format(
                                 multiprocessing.current_process().name, os.getpid()))

                data = connection.recv(BUFFER_SIZE)
                if not data:
                    connection.close()
                    self.logger.info("Connection from {} closed, cause no data received".format(address))
                    continue

                self.logger.info("\n%s", data)
                request = Request.create_request(data)
                response = str(RequestHandler(request, self.document_root).response)
                connection.sendall(response)
                connection.close()
            except socket.error:
                self.socket.close()
