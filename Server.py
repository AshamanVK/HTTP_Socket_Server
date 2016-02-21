#!/usr/bin/python2
"""Server main class."""

import socket


class HttpServer:
    """Server object."""

    def __init__(self, port=5000):
        """Constructor."""
        self.host = "localhost"
        self.port = port

    def server(self):
        """Main loop."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        print "start server on:", self.host, self.port
        while True:
            self.socket.listen(1)
            self.conn, self.addr = self.socket.accept()
            print "got connection from:", self.addr

            self.data = self.conn.recv(1024)
            print self.data

            r.http_request()
            r.get_headers()

            self.conn.send(self.data)
            self.conn.close()


class HttpRequest:
    """Parser."""

    def http_request(self):
        """Parse header."""
        self.method = s.data.split(" ")[0]
        print self.method

    def get_headers(self):
        """Headers."""
        temp = s.data.split("\r\n")
        self.headers = temp
        print self.headers


s = HttpServer()
r = HttpRequest()
s.server()
