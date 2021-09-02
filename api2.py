# -*- coding: utf-8 -*-
import gen2
from enum import Enum
import select


inputs = []
outputs = []
errors = []

def socket_listen(sock, msg):
    data = []
    while True:
        raw = sock.recv(4096)
        data.append(raw.decode('utf-8'))
        if len(raw) == 0:
            break
    return data

class St(Enum):
    AGAIN = 1
    CLOSE = 2
    FETCH = 3
    OPEN = 4
    GOOD = 5
    ERROR = 6

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

generators = map(gen2.generator, urls1)
tasks = {}

for task in generators:
    # 1
    addres, st = next(task)
    if st != St.GOOD:
        print(' ---> task close')
        task.close()

    # 3
    socket, st = next(task)
    if st != St.GOOD:
        print(' ---> task close')
        task.CLOSE()
    else:
        tasks[socket] = task
        outputs.append(socket)

while True:
    rsock, wsock, ersock = select.select(inputs, outputs, errors)
    
    for sock in rsock:
        # прием сообщенией.
        rep = socket_listen(sock)
        tasks[sock].send(rep)
        inputs.remove(sock)
        outputs.append(sock)
        
        
    for sock in wsock:
        # отправка сообщений
        msg, st = next(tasks[sock])
        if st == St.OPEN:
            sock.send(msg)
            inputs.append(sock)
            outputs.remove(sock)


    for sock in ersock:
        # удаление сокета.
        tasks[sock].close()
        sock.close()









