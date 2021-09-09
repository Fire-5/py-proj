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

class Status(Enum):
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

# generators = map(gen2.generator, urls1)
generators = [gen2.generator('https://api.github.com')]
tasks = {}

for task in generators:
    # 1
    addres, st = next(task)
    if st != Status.GOOD:
        print(st, ' ---> task close')
        task.close()

    # 2
    socket, st = next(task)
    if st != Status.GOOD:
        print(' ---> task close')
        task.close()
    else:
        tasks[socket] = task
        outputs.append(socket)

print(tasks)

while True:
    rsock, wsock, ersock = select.select(inputs, outputs, errors)
    
    for sock in rsock:
        # прием сообщенией.
        report = socket_listen(sock)
        tasks[sock].send(report) # 4
        
        msg, st = next(tasks[sock]) # 5
        if st == Status.FETCH:
            print(msg)
        if st == Status.CLOSE:
            inputs.remove(sock)
            errors.append(sock)
            
        inputs.remove(sock)
        outputs.append(sock)
        
        
    for sock in wsock:
        # отправка сообщений (3)
        msg, st = next(tasks[sock])
        if st == Status.OPEN:
            sock.send(msg)
            inputs.append(sock)
            outputs.remove(sock)
        if st == Status.CLOSE:
            inputs.remove(sock)
            errors.append(sock)
        


    for sock in ersock:
        # удаление сокета.
        print(' ---> task close')
        tasks[sock].close()
        sock.close()









