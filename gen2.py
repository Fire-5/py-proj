# -*- coding: utf-8 -*-
import enum
import socket
# import BeautifulSoup


class Status(enum.Enum):
    AGAIN = enum.auto()
    CLOSE = enum.auto()
    FETCH = enum.auto()
    OPEN  = enum.auto()
    GOOD  = enum.auto()
    ERROR = enum.auto()


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
    try:
        temp = report[0].split('\n')
        status = temp[0].split()
        return status[1]
    except:
        return '400'
    
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
    print(task_url[7:15], '1')
    # 1 Определение ip-адреса
    if 'https://' in task_url:
        PORT = '80'
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
    
    print(task_url[:8], '2')
    # 2 Подключение к сайту
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, int(PORT)))
        st = Status.GOOD
    except:
        print*(' ---> Error connect to {}'.format(task_url))
        st = Status.CLOSE
    finally:
        yield sock, st

    print(task_url[:8], '3')
    # 3 создание запроса
    message = request(task_url)
    yield message, Status.OPEN

    print(task_url[:8], '4')     
    # 4 Прием извне данных
    report = yield()
    st_report = check(report)

    print(task_url[:8], '5')
    # 5 Отправка обработанных данных
    str_None = 'None'
    if st_report != '200':
        yield str_None, Status.CLOSE
    
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
        yield str_None, Status.CLOSE
