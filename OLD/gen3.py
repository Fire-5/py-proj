# -*- coding: utf-8 -*-
import enum
import socket
import requests
import os


class Status(enum.Enum):
    START = enum.auto()
    GET = enum.auto()
    BAD = enum.auto()
    LOAD = enum.auto()
    ERROR = enum.auto()
    CLOSE = enum.auto()


def request(task_url):
    ''' старая версия функции, которая собирает HTTP-запрос GET 
    из строки. В целом работает, но почти все сайты видят 
    этот вариант ошибочным (код ошибки 400)'''

    r = requests.Request('GET', task_url)
    req = r.prepare()
    request = f"""GET {req.path_url} HTTP/1.1\r\n
    HOST: {task_url}\r\n
    User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)\r\n
    Accept: */*\r\n
    Connection: Keep-Alive\r\n
    \r\n\r\n"""
    message = request.encode('utf-8')
    status = Status.GET
    print(message)
    return message, status


def read_data(raw_data):
    print('[CHECK] ::', raw_data)
    return [], Status.ERROR


def setup_url(task_url, PORT):
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        HOST = socket.gethostbyname(task_url)
        print(HOST, PORT)
        _socket.connect((HOST, PORT))
        st = Status.START

    except Exception as _exc1:
        print(f' ---> [ERROR] Error connect to {task_url}\n{_exc1}')
        st = Status.ERROR

    finally:
        return _socket, st


def generator(raw_url):
    # Получение и обработка адреса для запроса 

    if 'https://' in raw_url:
        PORT = 433
        task_url = raw_url[8:]
    elif 'http://' in raw_url:
        PORT = 80
        task_url = raw_url[7:]

    print(f' ---> {task_url} Step 0')

    # 0 Возвращаем из генератора сокет
    socket, status = setup_url(task_url, PORT)
    yield socket, status

    print(f' ---> {task_url} Step 1')
    # 1
    message, status = request(raw_url)
    yield message, status

    print(f' ---> {task_url} Step 2')

    # 2
    raw_data = yield  # ????????????
    print(f'[R] {type(raw_data)}')

    print(f' ---> {task_url} Step 3')
    # 3
    pack, Status.LOAD = read_data(raw_data)

    # print(f' ---> {task_url} Step 4')
    # for img_url in pack:
    #     # 4
    #     yield img_url, status
    #     # 5
    #     data_img = yield()
    #     # ....

    # print(f' ---> {task_url} Finish!')
    # 7
    status = Status.CLOSE
    yield None, status
    yield None, status
