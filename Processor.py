#!/usr/bin/python2

import socket

request_data = []


def request_data_clear():
    '''Clear all saved request_data'''

    global request_data
    request_data = []


def line_format(s):
    '''Convert all line endings in request to \n'''

    return ''.join((line + '\n') for line in s.splitlines())


def recv_all(sock):
    '''Read all data from request'''

    timeout = sock.gettimeout()
    try:
        sock.settimeout(0.1)

        data = []
        while True:
            try:
                data.append(sock.recv(1024))
            except socket.timeout:
                return ''.join(data)

    finally:
        sock.settimeout(timeout)


def get_request_data(socket):

    request = line_format(recv_all(socket))
    request_body = request.split('\n\n', 1)

    # IGNORE /favicon.ico
    temp = request_body[0].splitlines()
    temp_list = temp[0].split(' ')
    if temp_list[1] == '/favicon.ico':
        print '##STEP_1_and_2_IGNORED---------------------'
        print 'SORRY BUT FAVICON WAS IGNORED'
        return
    else:
        if len(request_data) != 1:
            request_data_clear()
        request_data.append(request_body)

    print '##STEP_1<<<<<<<<<<request>>>>>>>>>>>>>>>>>>'
    print request
    print '>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<'

    print '##STEP_2--------request_data---------------'
    for i in request_data:
        print i
    return request_data


def parse_data():

    request_head = request_data[0][0].splitlines()
    request_headline = request_head[0]
    request_headers = dict(x.split(': ', 1) for x in request_head[1:])

    request_method, request_url, request_proto = request_headline.split(' ', 3)

    print '##STEP_3-----request_healine---------------'
    print request_headline
    print '##STEP_4-----request_headers---------------'
    print request_headers
