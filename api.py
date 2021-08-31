# -*- coding: utf-8 -*-
"""
в один поток много хттп-запросов
генератор - запрос - сокет - сеть
http = 80, https = 443


    1. подключение, проверка статуса
    2. парсим данные
    3. скачиваем картинки
    4. закрываем

"""

import select
import socket
import gen
from gen import Status

inputs = []
outputs = []
excepts = []


def socket_create(addr):
    HOST, PORT = addr.split(':')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, int(PORT)))
    inputs.append(sock)
    return sock



urls1 = ['https://api.github.com', 'https://mail.ru']
urls2 = [
    'http://www.google.com',
    'http://www.yandex.ru',
    'http://www.python.org',
    'https://vk.com',
    'https://www.youtube.com',
    'https://mail.ru',
    'http://tapochek.net'
]

generators = map(gen.generator, urls1)

for task in generators:
    addr, status = next(task)
    if status != Status.GOOD:
        task.close()
        break
    
    sock = socket_create(addr)
    task.send(sock)
    next(task)
    print('/n/n/n/n')
    
    

# reads, send, excepts = select.select(inputs, outputs, excepts)

# while True:
#     for sock in reads:
#         pass
