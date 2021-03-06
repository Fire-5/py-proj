#!python3.6
# -*- coding: utf-8 -*-

'''
Генератор — это объект, который сразу при создании не вычисляет 
значения всех своих элементов. Он хранит в памяти только последний 
вычисленный элемент, правило перехода к следующему и условие,
при котором выполнение прерывается. Вычисление следующего значения 
происходит лишь при выполнении метода next(). 
Предыдущее значение при этом теряется.

(выражение for j in итерируемый объект if условие)
Где for, in, if — ключевые слова, j — переменная.

next() - следующая итерация
close() — останавливает выполнение генератора
throw() — генератор бросает исключение
send() — интересный метод, позволяет отправлять значения генератору

Перехват итераций:
while True:
    try:
    	...
        coroutine.send(None)  # В четвёртый раз здесь вылетит StopIteration
    except StopIteration:
        break				  # Здесь обрываемся, или продолжаем, или...

'''
from enum import Enum
import socket


class Status(Enum):
    AGAIN = 1
    CLOSE = 2
    FETCH = 3
    OPEN = 4
    GOOD = 5
    ERROR = 6


def request(task_url):
    req = """
GET / HTTP/1.1
Host: {}
Accept: text/html
Connection: close
\r
\r
""".format(task_url)
    req = req.encode('utf-8')
    return req


def socket_call(sock, msg):
    sock.send(msg)
    data = []

    while True:
        raw = sock.recv(4096)
        data.append(raw.decode('utf-8'))
        if len(raw) == 0:
            break

    return data


def socket_create(addr):
    HOST, PORT = addr.split(':')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, int(PORT)))
    return sock


def generator(task_url):
    '''
    1. выявление адреса, сборка запроса
    2. Получение сокета, подключение, проверка статуса
    2. Если ок, парсим данные
    3. Отправляем набор ссылок на картинки
    4. закрываем

    '''
    # 1 выявление адреса, сборка запроса
    if 'https://' in task_url:
        PORT = '443'
        task_url = task_url[8:]
    elif 'http://' in task_url:
        PORT = '80'
        task_url = task_url[7:]

    req = request(task_url)
    try:
        HOST = socket.gethostbyname(task_url)
        yield HOST + ':' + PORT, req, Status.GOOD
    except:
        HOST = '127.0.0.1'
        yield HOST + ':' + PORT, req, Status.ERROR

    # 2 получение сокета
    sock = socket_create(HOST + ':' + PORT)
    yield sock, Status.GOOD
    
    data = socket_call(sock, req)
    stat = data
    yield stat, Status.GOOD


#
#     # Парсим data
#     payload = bs.parse(data)
#     # возвращаем задание или даже новую пачку генераторов другого типа
#     yield (...)
#     # Получаем и работаем
#     ...
#     # тут вместо сокета отдаём None => таска готова
#     yield (None, data_to_print)

# def upload_img(tsk_url):
#         '''
#     1. выявление айпи
#     2. Получение сокета, подключение, проверка статуса
#     2. Если ок, парсим данные
#     3. Отправляем набор ссылок на картинки
#     4. закрываем

#     '''
