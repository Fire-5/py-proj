# -*- coding: utf-8 -*-
import enum
import socket
import requests



class Status(enum.Enum):
    AGAIN = enum.auto()
    CLOSE = enum.auto()
    FETCH = enum.auto()
    OPEN  = enum.auto()
    GOOD  = enum.auto()
    ERROR = enum.auto()


# def request(task_url):
# ''' старая версия функции, которая собирает HTTP-запрос GET 
# из строки. В целом работает, но почти все сайты видят 
# этот вариант ошибочным (код ошибки 400)'''

#     req = """GET / HTTP/1.1
# User-Agent: python-requests/2.26.0
# Accept-Encoding: gzip, deflate
# Accept: */*
# Connection: keep-alive
# \r
# \r
# """.format(task_url)
#     req = req.encode('utf-8')
#     return req

def request(task_url):
    ''' обновленная версия метода создания запроса к сайту.
    Используется библиотека Requests. В данном варианте
    ответы на запрос возвращаются с ошибкой 400'''

    r = requests.Request('GET', task_url)
    req = r.prepare()
    request = """{} {} HTTP/1.1
Host: developer.mozilla.org

""".format(req.method, req.path_url, req.url)
    request = request.encode('utf-8')
    return request

def check(report):
    ''' метод проверки кода ответа на запрос'''

    try:
        temp = report[0].split('\n')
        status = temp[0].split()
        return status[1]
    except:
        return '400'
    
def parsing(report):
    ''' метод обработки входящего сообщения. 
    Кустарно реализовано отсечение заголовков от тела ответа'''  

    try:
        data = report.split('\n')
        n_body = 0
        for ind, item in enumerate(data):
            if item == '\r':    
                n_body = ind + 1
                print(n_body)
                
        for i in range(n_body):
            l = data.pop(0)
        return data
    except:
        return "No data"

def generator(raw_url):
    ''' Функция-генератор, которая контролирует все действия к сайту,
    формирует запросы и парсит данные отправляя наружу 
    только нужный объект данных и статус'''

    print("{:<25} {}".format(raw_url, 'Step 1\r'))
    # 1 Определение ip-адреса
    if 'https://' in raw_url:
        PORT = '80'
        task_url = raw_url[8:]
    elif 'http://' in raw_url:
        PORT = '80'
        task_url = raw_url[7:]

    try:
        HOST = socket.gethostbyname(task_url)
        yield HOST + ':' + PORT, Status.GOOD
    except:
        HOST = '127.0.0.1'
        yield HOST + ':' + PORT, Status.CLOSE
    
    print("{:<25} {}".format(raw_url, 'Step 2\r'))
    # 2 Подключение к сайту
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, int(PORT)))
        st = Status.GOOD
    except:
        print(' ---> Error connect to {}'.format(task_url))
        st = Status.CLOSE
    finally:
        yield sock, st

    print("{:<25} {}".format(raw_url, 'Step 3\r'))
    # 3 создание запроса
    message = request(raw_url)
    yield message, Status.OPEN

    print("{:<25} {}".format(raw_url, 'Step 4\r'))    
    # 4 Прием извне данных
    report = yield()
    
    # 5 Отправка обработанных данных
    st_report = check(report)
    str_None = 'None'
    if st_report != '200':
        yield str_None, Status.CLOSE

    print ("{:<25} {}".format(raw_url, 'Stepи 5 '), st_report)    
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
        print ("{:<25} {}".format(raw_url, 'FINISH'))
        yield urls, Status.FETCH

        
    else:
        yield str_None, Status.CLOSE

    print ("{:<25} {}".format(raw_url, 'ERROR'))
    yield 'Finish', Status.CLOSE