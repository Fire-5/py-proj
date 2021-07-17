# -*- coding: utf-8 -*-
import socket
import time

def connect_socket(addr):
    print('... connect ...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(addr)
    print('... connected!')

############################################################

def send_socket(sock, param):
    if param == 'open':
        Code = 200
        Desc = 'Connect'
        Conn = 'await'
        Text = 'Wait messages'

    elif param == 'close':
        Code = 200
        Desc = 'Connect'
        Conn = 'Close'
        Text = 'Close connection'

    elif param == 'text':
        Code = 200
        Desc = 'Connect'
        Conn = 'await'
        Text = 'The message is received'
    else:
        Code = 400
        Desc = 'Disconnect'
        Conn = 'Close'
        Text = 'Error'

    Date = time.ctime(time.time())
    resp = '''HTTP/1.1 {} {}
    Content-Type: text; charset=UTF-8
    Content-Length: {}
    Date: {}
    Connection: {}

    <text>{}<text/>'''
    resp = resp.format(Code, Desc, len(resp),
                       Date, Conn, Text)
    sock.send(resp.encode())

############################################################

def del_socket(sock, inputs, outputs):
    send_socket(sock, 'close')
    if sock in inputs:
        inputs.remove(sock)
    if sock in outputs:
        outputs.remove(sock)
    sock.close()

############################################################

def listen_socket(sock):
    data = ''
    while True:
        temp = sock.recv(1024)
        data = data + temp.decode('utf-8')
        if temp == '':
            break
    return data

############################################################

def search_text(sock, data):
    for line in data:
        if '<text>' in line:
            text_data = line[5:-6]
    return text_data

############################################################
