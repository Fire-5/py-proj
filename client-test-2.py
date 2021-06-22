# -*- coding: utf-8 -*-
import socket

print('Для выхода из чата наберите: `exit`, `quit` или `q`.')
# Удаленный хост
HOST = '127.0.0.1'
# тот же порт, что и у сервера
PORT = 8008

name = input('\nВведите ваше имя: ')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        mess = input(' >>> ')

        if any(mess.lower() in ext for ext in ['quit', 'exit', 'q']):
            break
        message = name + ' : '+ mess
        message = message.encode('utf-8')
        s.sendall(message)
        data = s.recv(1024)
        print(data.decode('utf-8'))