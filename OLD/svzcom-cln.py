# -*- coding: utf-8 -*-

import select
import socket
import time

print(' >>> start <<< ')

HOST = '127.0.0.1'  # Удаленный хост
PORT = 8008         # тот же порт, что и у сервера
local_time = time.ctime(time.time())

inputs = [socket] # сокеты, которые будем читать
outputs = []    # сокеты, в которые надо писать


def dispetcher():
    addr = (HOST, PORT)
    text_line = client_gen(addr)
    while True:
        text = next(text_line)
        print(text)

    return 'Done'

def client_gen(addr):
    # Подключение
    print('... connect ...')
    Date = time.ctime(time.time())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(addr)
        print('... connected!')
        message = '''GET / HTTP/1.1
        Host: localhost
        Accept: text
        Content-Length: {}
        Date: {}
        Connection: {}

        <text>{}<text/>
        '''
        message.format(len(message), Date, 'await', 'Hello world!')
        s.sendall(message.encode('utf-8'))
        text = s.recv(1024)
        print(text.decode('utf-8'))
        yield text

        # Передача информации
        print('... send text ...')
        message.format(len(message), Date, 'await',
                       'V lesu rodilas` yelochka')
        s.sendall(message.encode('utf-8'))
        text = s.recv(1024)
        print(text.decode('utf-8'))
        yield text

        # Отключеение
        print('... client out line ...')
        message.format(len(message), Date, 'Close', 'Client out line')
        s.sendall(message.encode('utf-8'))
        text = s.recv(1024)
        print(text.decode('utf-8'))
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