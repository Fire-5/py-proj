# -*- coding: utf-8 -*-

import select
import socket
import time
import random as r
import argparse

def search_text(sock, data):
    for line in data:
        if '<text>' in line:
            text_data = line[5:-6]
    return text_data

def send_message(sock, param):
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

def del_socket(sock, inputs, outputs):
    send_message(sock, 'close')
    if sock in inputs:
        inputs.remove(sock)
    if sock in outputs:
        outputs.remove(sock)
    sock.close()

def listen_socket(sock):
    data = ''
    while True:
        temp = sock.recv(1024)
        data = data + temp.decode('utf-8')
        if temp == '':
            break
    return data

################################################################
local_time = time.ctime(time.time())
IP = 'localhost'
PORT = 8008

# Создание нового аргумента для запуска файла программы.
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port',
                    help='Port to use, defaults to {}'.format(PORT),
                    default=8008, type=int)
args = parser.parse_args()

# Вывод основного аргумента
print("Using a addres: {}:{}".format(IP, PORT))



sock = socket.socket()
sock.bind((IP, PORT))
sock.listen(5)
sock.setblocking(False)

inputs = [sock] # сокеты, которые будем читать
outputs = []    # сокеты, в которые надо писать
messages = []   # здесь будем хранить сообщения для сокетов



# response = '''HTTP/1.1 {} {}
# Content-Type: text; charset=UTF-8
# Content-Length: {}
# Date: {}
# Connection: {}

# <text>{}<text/>'''
# print(response.format('400', 'Bad Request', len(response), local_time, 'close'))

print('START')
while True:
    Code = 200
    Desc = 'Connect'
    Connection = 'Open'
    Date = local_time

    # вызов `select.select`
    reads, send, excepts = select.select(inputs,
                                         outputs,
                                         inputs)

    # список READS - сокеты, готовые к чтению
    for conn in reads:
        if conn == socket:
            # если это серверный сокет, то пришел новый
            # клиент, принимаем подключение
            new_conn, client_addr = conn.accept()
            print(local_time, '> Успешное подключение от:',
                  client_addr)
            new_conn.listen()
            new_conn.setblocking(False)
            inputs.append(new_conn)

        else:
            # если это НЕ серверный сокет, то
            # клиент хочет что-то сказать
            # data = listen_socket(conn)
            data = ''
            temp = sock.recv(1024)
            data = data + temp.decode('utf-8')
            print(local_time, '> Клиент прислал сообщение...')
            text_data = search_text(conn, data)
            print(local_time, '> {}'.format(text_data))
            if conn not in outputs:
                outputs.append(conn)

            else:
                print(local_time, '> Клиент отключился...')
                # если сообщений нет, то клиент закрыл соединение
                # удаляем его сокет из всех очередей
                del_socket(conn, inputs, outputs)


    # список SEND - сокеты, готовые принять сообщение
    for conn in send:
        print(local_time, '> Отправляю ответ...')
        if text_data == 'Hello world!':
            send_message(sock, 'open')
        else:
            send_message(sock, 'text')

        outputs.remove(conn)



    # список EXCEPTS - сокеты, в которых произошла ошибка
    for conn in excepts:
        # удаляем сокет с ошибкой из всех очередей
        del_socket(conn, inputs, outputs)



print('CLOSE')