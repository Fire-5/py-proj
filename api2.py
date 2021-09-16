# -*- coding: utf-8 -*-
import select
import gen2


def socket_listen(sock):
    ''' метод приема данных и формирование их в массив данных'''
    data = []
    chance = 0
    while True:
        raw = sock.recv(128)
        try:
            data.append(raw.decode('utf-8'))
            if len(raw) == 0:
                break
        except UnicodeDecodeError as e:
            # print(' ---> Unicode Error!')
            continue
    return data


def task_setup(task):
    ''' метод, который  создает генератор и готовит его
    к отправвке первого запроса.'''
    
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


Status = gen2.Status

inputs = []
outputs = []
errors = []

urls1 = ['https://developer.mozilla.org']
urls2 = [
    'http://www.google.com',
    'http://www.yandex.ru',
    'http://www.python.org',
    'https://vk.com',
    'https://www.youtube.com',
    'http://tapochek.net'
]

generators = map(gen2.generator, urls1)    # Вариант 1
# generators = map(gen2.generator, urls2)   # Вариант 2
tasks = {}

for task in generators:
    task_setup(task)

# Реализация селект-запроса
while True:
    rsock, wsock, ersock = select.select(inputs, outputs, errors)
    
    for sock in rsock:
    # прием сообщенией.
        report = socket_listen(sock)

        # 4 Отправка в генератор
        tasks[sock].send(report) 

        # 5 отчет от генератора
        msg, st = next(tasks[sock]) 
        if st == Status.FETCH:
            print(msg)
        
        if st == Status.CLOSE:
            errors.append(sock)

        outputs.append(sock)
        inputs.remove(sock)
        
    for sock in wsock:
    # отправка сообщений
        # 3 получение запроса от генератора
        msg, st = next(tasks[sock])
        # print(' ---> ', msg, st)
        if st == Status.OPEN:
            sock.send(msg)
            inputs.append(sock)
            outputs.remove(sock)
        if st == Status.FETCH:
            print(type(msg))
            print(' ---> GOOD')
        if st == Status.CLOSE:
            errors.append(sock)
            outputs.remove(sock)
        
    for sock in ersock:
    # удаление сокета.
        inputs.remove(sock)
        outputs.remove(sock)
        print(' ---> task close')
        tasks[sock].close()
        sock.close()
