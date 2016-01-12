#!usr/bin/python2

import socket
import Processor


def main():
    '''Server main loop'''

    host = 'localhost'
    port = 5000

    try:
        server_sock = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM,
                                    socket.IPPROTO_TCP)
        server_sock.setsockopt(socket.SOL_SOCKET,
                               socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(1)
        print 'Server start listen at:\n', str(host) + ':' + str(port)
    except socket.error as msg:
        print 'Oops! we have an error here...\n', msg
        main()

    while True:
        client_sock, cliet_addr = server_sock.accept()

        Processor.get_request_data(client_sock)
        Processor.parse_data()

        print '##STEP_5-----sending_response--------------'
        print 'response to connection: HI! how are you?\n'
        client_sock.send('HI! how are you?\n')

        Processor.set_flow_free()

        client_sock.close()


if __name__ == '__main__':
    main()
