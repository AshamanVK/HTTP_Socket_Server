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

            self.data = c.data

            r = HttpRequest(self.data)
            r.http_request()
            r.get_headers()

            c.conn.send("Hi!")
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
        except:
            pass
        print self.data


class HttpRequest:
    """Parser."""

    def __init__(self, data):
        """Constructor."""
        self.data = data
        self.head = data.split("\n\n")[0]
        self.headers = {}
        try:
            self.body = data.split("\n\n")[1]
        except:
            pass

    def http_request(self):
        """Parse header."""
        self.method = self.head.split(" ")[0]

    def get_headers(self):
        """Headers."""
        for i in self.head.splitlines():
            try:
                temp = i.split(": ")
                self.headers[temp[0]] = temp[1]
            except:
                pass


s = HttpServer()
s.serve()
