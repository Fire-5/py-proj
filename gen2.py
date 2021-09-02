# -*- coding: utf-8 -*-
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


def generator(task_url):
    # 1 Определение ip-адреса
    if 'https://' in task_url:
        PORT = '443'
        task_url = task_url[8:]
    elif 'http://' in task_url:
        PORT = '80'
        task_url = task_url[7:]

    try:
        HOST = socket.gethostbyname(task_url)
        yield HOST + ':' + PORT, Status.GOOD
    except:
        HOST = '127.0.0.1'
        yield HOST + ':' + PORT, Status.CLOSE
    
    # # 2 Составление HTTP запроса.
    # req = request(task_url)
    # yield req, Status.GOOD

    # 3 Подключение к сайту
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, int(PORT)))
        yield sock, Status.GOOD
    except:
        print*(' ---> Error connect to {}'.format(task_url))
        yield sock, Status.CLOSE
        
    # 4
    report = yield
    imgs = parsing(report)
    
    
    
    
    
    
    
    
    
    
    
    
    
    