# -*- coding: utf-8 -*-
from enum import Enum
import socket
# import BeautifulSoup


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

def check(report):
    temp = report.split('\n')
    status = temp[0].split()
    return status[1]
    
def parsing(report):
    data = report.split('\n')
    n_body = 0
    for ind, item in enumerate(data):
        if item == '\r':
            n_body = ind + 1
            print(n_body)
            
    for i in range(n_body):
        l = data.pop(0)
        print(i, l)
    return data

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
    
    # 2 Подключение к сайту
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, int(PORT)))
        yield sock, Status.GOOD
    except:
        print*(' ---> Error connect to {}'.format(task_url))
        yield sock, Status.CLOSE
        
    # 3
    message = request(task_url)
    yield message, Status.GOOD
        
    # 4
    report = yield
    
    st_report = check(report)
    # 5
    if st_report != '200':
        yield None, Status.CLOSE
    
    dt_report = parsing(report)
    if 'img' in dt_report:

        urls = []
        copy_dt = dt_report.copy()
        for line in copy_dt:
            if "img" in line:
                line.lstrip('<img src=')
                line.rstrip('>')
                line = task_url + "/" + line
                urls.append(line)
        yield urls, Status.FETCH
        
    else:
        yield None, Status.CLOSE
         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    