#!/usr/bin/python2
"""Server main class."""

import socket


class HttpServer:
    """Server object."""

    def __init__(self, port=5000):
        """Constructor."""
        self.host = "localhost"
        self.port = port
        self.data = ""

    def serve(self):
        """Main loop."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print "start server on:", self.host, self.port

        while True:

            c = HttpConnection(self.socket)
            c.connection()

            parse = HttpRequestParser(c.data)
            parse.get_method()
            parse.get_headers()
            parse.get_body()

            request = HttpRequest(parse.method,
                                  parse.headers,
                                  parse.body)
            request.test()

            c.conn.send(c.data)
            c.conn.close()


class HttpConnection:
    """New connection."""

    def __init__(self, socket):
        """Constructor."""
        self.socket = socket
        self.conn, self.addr = self.socket.accept()
        self.data = ""

    def connection(self):
        """Making new connection."""
        print "got connection from:", self.addr
        self.conn.settimeout(0.5)
        try:
            while True:
                temp = self.conn.recv(1024)
                self.data += temp
                if not temp:
                    break
        except socket.timeout:
            pass
        print self.data
        print self.data.split("\n\n")


class HttpRequest:
    """Parser."""

    def __init__(self, method, headers, body):
        """Constructor."""
        self.method = method
        self.headers = headers
        self.body = body

    def test(self):
        """Test."""
        print "-----------"
        print self.method
        print "-----------"
        print self.headers
        print "-----------"
        print self.body
        print "-----------\n\n\n"


class HttpRequestParser:
    """Request parser."""

    def __init__(self, data):
        """Constructor."""
        self.data = data
        self.head = data.split("\r\n\r\n")[0]
        self.headers = {}
        self.body = []

    def get_method(self):
        """Method string."""
        self.method = self.head.split(" ")[0]

    def get_headers(self):
        """Header dictionary."""
        for i in self.head.splitlines():
            try:
                temp = i.split(": ")
                self.headers[temp[0]] = temp[1]
            except IndexError:
                pass

    def get_body(self):
        """Body list."""
        try:
            self.body = self.data.split("\r\n\r\n")[1]
        except IndexError:
            pass

s = HttpServer()
s.serve()
