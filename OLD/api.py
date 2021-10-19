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

urls1 = ['https://api.github.com']
urls2 = [
    'http://www.google.com',
    'http://www.yandex.ru',
    'http://www.python.org',
    'https://vk.com',
    'https://www.youtube.com',
    'https://mail.ru',
    'http://tapochek.net'
]

generators = map(gen.generator, urls2)

for task in generators:
    # 1 выявление адреса, сборка запроса
    addr, msg, status = next(task)
    if status != Status.GOOD:
        task.close()
        break
    
    # 2 получение сокета
    sock, status = next(task)
    if status != Status.GOOD:
        task.close()
        break
    

    stat, status = next(task)
    if status != Status.GOOD:
        task.close()
        break
    print(stat)
    
    

# 

# while True:
#     for sock in reads:
#         pass
