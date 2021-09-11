# -*- coding: utf-8 -*-
import select

import gen2


def socket_listen(sock):
    data = []
    chance = 0
    while True:
        raw = sock.recv(4096)
        # data.append(raw.decode('utf-8'))
        data = raw.decode('utf-8')
        if len(raw) == 0:
            break
    return data


Status = gen2.Status

inputs = []
outputs = []
errors = []

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

generators = map(gen2.generator, urls2)
# generators = [gen2.generator('https://api.github.com')]
tasks = {}

for task in generators:
    # 1 Определение ip-адреса
    addres, st = next(task)
    if st != Status.GOOD:
        print(st, ' ---> task close')
        task.close()

    # 2 Подключение к сайту
    socket, st = next(task)
    if st != Status.GOOD:
        print(' ---> task close')
        task.close()
    else:
        tasks[socket] = task
        outputs.append(socket)

print('>>>', tasks)
print()

while True:
    rsock, wsock, ersock = select.select(inputs, outputs, errors)
    
    for sock in rsock:
        # прием сообщенией.
        report = socket_listen(sock)
        print('>>> \n\n', report, '\n\n')
        local_task = tasks[sock]
        local_task.send(report) # 4 Отправка в генератор

        local_task = tasks[sock]
        msg, st = next(local_task) # 5 отчет от генератора
        if st == Status.FETCH:
            print(msg)
        
        if st == Status.CLOSE:
            errors.append(sock)

        outputs.append(sock)
        
    for sock in wsock:
        # отправка сообщений
        # 3 получение запроса от генератора
        # print('>>>', type(tasks[sock]))

        local_task = tasks[sock]
        msg, st = next(local_task)
        if st == Status.OPEN:
            sock.send(msg)
            inputs.append(sock)
            

        if st == Status.CLOSE:
            errors.append(sock)
        
    for sock in ersock:
        # удаление сокета.
        inputs.remove(sock)
        outputs.remove(sock)
        print(' ---> task close')
        tasks[sock].close()
        sock.close()
