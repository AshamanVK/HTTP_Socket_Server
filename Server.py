# -*- coding: utf-8 -*-
u"""HTTP Сервер."""

import socket
import time


class HttpServer:
    u"""Объект сервера."""

    def __init__(self, port=5000):
        u"""Значения по умолчанию."""
        self.host = "localhost"
        self.port = port
        self.data = ""

    def serve(self):
        u"""Запуск сервера."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print "start server on:", self.host, self.port

        while True:

            self.conn, self.addr = self.socket.accept()

            # создаем объект - подключение
            c = HttpConnection(self.conn, self.addr)
            # считываем данные подключения
            data = c.connection()

            # создаем объект обрабатывающий данные
            parse = HttpRequestParser(data)
            # передаем разделенные данные дальше в реквест
            parse.get_request()

            parse.request.test()  # принт полученных данных
            answer = parse.request.do_something()

            snd = HttpResponse(c.conn, self.addr, answer)

            response = snd.send_to_client()

            c.conn.send("\n" + response)
            c.conn.close()


class HttpConnection:
    u"""Получение данных из входящего соединения."""

    def __init__(self, conn, addr):
        """noflake8."""
        self.conn = conn
        self.addr = addr
        self.data = ""

    def connection(self):
        u"""Считывание данных полученных от клиента."""
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
        return self.data


class HttpRequestParser:
    u"""Разбор данных на составляющие."""

    def __init__(self, data):
        """Constructor."""
        self.data = data
        self.head = data.split("\r\n\r\n")[0]
        self.headers = {}
        self.body = ""

    def __get_method(self):
        u"""Достаем первую строку запроса."""
        self.method = self.head.split("\r\n")[0]
        self.method = self.method.split(" ")

    def __get_headers(self):
        u"""Формируем словарь из хедеров."""
        for i in self.head.splitlines():
            time.sleep(.1)
            try:
                temp = i.split(": ")
                self.headers[temp[0]] = temp[1]
            except IndexError:
                pass

    def __get_body(self):
        u"""Если клиент рередал данные, записываем их."""
        try:
            self.body = self.data.split("\r\n\r\n")[1]
        except IndexError:
            pass

    def get_request(self):
        u"""Создаем объект HttpRequest.

        Передаем ему (list, dict, string).
        """
        self.__get_method()
        self.__get_headers()
        self.__get_body()
        self.request = HttpRequest(self.method,
                                   self.headers,
                                   self.body)


class HttpRequest:
    u"""Обработка полученых данных."""

    def __init__(self, method, headers, body):
        u"""Получаем (list, dict, str)."""
        self.method = method
        self.headers = headers
        self.body = body
        self.answer = "good"

    def do_something(self):
        """noflake8."""
        head_list = self.__make_headers_list()

        request_method = self.method[0]

        if request_method not in ["POST", "GET"]:
            self.answer = "400"
            return (self.answer, head_list)

        return (self.answer, head_list)

    def __make_headers_list(self):
        u"""Из словаря хедеров делаем список."""
        temp = [k + ": " + v for (k, v) in self.headers.items()]
        return temp

    def test(self):  # смотрю что и как лежит
        """Test."""
        print "-----------"
        print self.method
        print "-----------"
        print self.headers
        print "-----------"
        print self.body
        print "-----------"


class HttpResponse:
    u"""Ответ клиенту."""

    def __init__(self, conn, addr, answer):
        """noflake8."""
        self.conn = conn
        self.addr = addr
        self.answer = answer
        self.code = "200 OK"

    def send_to_client(self):
        """noflake8."""
        print self.answer           # принт для себя
        send = self.__template()
        print send
        print "-----------\n\n\n"
        return "\r\n".join(send)

    def __template(self):
        date = time.asctime()
        template = ["HTTP/1.1 " + self.code,
                    "Date: " + date]
        template += self.answer[1]
        return template

    def __200_ok(self):
        self.code = "200 OK"
        pass

    def __400_bad_request(self):
        self.code = "400 Bad Request"
        pass

    def __404_not_found(self):
        self.code = "404 Not Found"
        pass

s = HttpServer()
s.serve()
