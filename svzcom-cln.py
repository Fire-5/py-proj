# -*- coding: utf-8 -*-

import select
import socket
import time

print(' >>> start <<< ')

IP = '127.0.0.1'  # Удаленный хост
PORT = 8008         # тот же порт, что и у сервера
local_time = time.ctime(time.time())

inputs = [socket] # сокеты, которые будем читать
outputs = []    # сокеты, в которые надо писать


def dispetcher():
    addr = (IP, PORT)
    text_line = client_gen(addr)
    while True:
        text = next(text_line)
        print(text)

    return 'Done'

def client_gen(addr):
    # Подключение
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(addr)
    send_message(sock, 'open')

    data = listen_socket(sock)
    text = search_text(sock, data)
    yield text

    # Передача информации
    send_message(sock, 'text')
    data = listen_socket(sock)
    text = search_text(sock, data)
    yield text

    # Отключеение
    send_message(sock, 'text')
    data = listen_socket(sock)
    text = search_text(sock, data)
    yield text

def listen_socket(sock):
    data = sock.recv(1024).decode('utf-8')
    # if data:
    #     for line in data:
    #         print('> ',line)
    return data

def search_text(sock, data):
    for line in data:
        if '<text>' in line:
            text_data = line[5:-6]
    return text_data

def send_message(sock, param):
    if param == 'open':
        Conn = 'await'
        Text = 'Hello world!'

    elif param == 'close':
        Conn = 'Close'
        Text = 'Client out line'

    elif param == 'text':
        Conn = 'await'
        Text = 'V lesu rodilas` yelochka'

    else:
        Conn = 'Close'
        Text = 'Error'

    Date = time.ctime(time.time())
    request = '''GET / HTTP/1.1
    Host: localhost
    Accept: text
    Content-Length: {}
    Date: {}
    Connection: {}

    <text>{}<text/>
    '''
    request = request.format(len(request), Date, Conn, Text)
    sock.send(request.encode())

if __name__ == '__main__':

    res = dispetcher()
    print(res)