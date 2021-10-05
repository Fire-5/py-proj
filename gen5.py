import socket
import enum
import os

import requests as requests
from bs4 import BeautifulSoup as bs


class Status(enum.Enum):
    START = enum.auto()
    GET = enum.auto()
    ERROR = enum.auto()
    CLOSE = enum.auto()
    READY = enum.auto()
    LOAD = enum.auto()


def setup_generator(generators_list):
    tasks = {}
    outputs = []
    for task in generators_list:
        # 1
        sock, st = next(task)
        if st != Status.START:
            print(f"[ERROR] Status: {st}\nTask error in step 1")
            task.close()

        else:
            tasks[sock] = task
            outputs.append(sock)

    return outputs, tasks


def parser(url, raw_data):
    data = raw_data.split('\r\n\r\n')[1]
    img_list = []
    soup = bs(data, 'html.parser')
    # print(f'[!!!] \n{soup}')
    for tag in soup.find_all("img"):
        print(f" ---> {url + tag['src']}")
        img_list.append([url + tag['src'], tag['id']])

    return img_list

def request(task_url):
    """ старая версия функции, которая собирает HTTP-запрос GET
    из строки. В целом работает, но почти все сайты видят
    этот вариант ошибочным (код ошибки 400)"""

    r = requests.Request('GET', task_url)
    req = r.prepare()
    url = task_url.replace(req.path_url, '')
    url = url.replace('https://', '')
    url = url.replace('http://', '')

    request = f"""GET {req.path_url} HTTP/1.1\r\n
    HOST: {url}\r\n
    User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)\r\n
    Accept: text\r\n
    Connection: Keep-Alive\r\n
    \r\n\r\n"""
    message = request.encode('utf-8')
    # print(message)
    return message


def setup_url(raw_url):
    if 'https://' in raw_url:
        PORT = 433
        task_url = raw_url[8:]
    elif 'http://' in raw_url:
        PORT = 80
        task_url = raw_url[7:]

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        HOST = socket.gethostbyname(task_url)
        print(f'[T] Connect to: {HOST}:{PORT}')
        _socket.connect((HOST, PORT))
        st = Status.START

    except Exception as _exc1:
        print(f' ---> [ERROR] Error connect to {task_url}\n{_exc1}')
        st = Status.ERROR

    finally:
        return _socket, st


def generator(raw_url):
    # 0
    print(f'[+] Task URL: {raw_url}')

    # 1
    sock, st = setup_url(raw_url)
    yield sock, st
    print(f'[+] Step 1: Connect done!')

    # 2
    msg = request(raw_url)
    print(f'[+] Step 2: Message send!')
    yield msg, Status.GET

    # 3
    raw_data = yield None, Status.READY
    print(f'[+] Download data:\n{raw_data[:16]}')
    img_list = parser(raw_url, raw_data)

    if len(img_list) > 0:
        for img in img_list:
            # 2
            msg = request(img[0])
            print(f'[+] Step 2: Message send!')
            yield msg, Status.GET
            yield msg, Status.GET

            image = yield None, Status.READY
            print(f'[+] Download data:\n{image[:16]}')

            if not os.path.exists(f'data//{raw_url[8:]}'):
                os.mkdir(f'data//{raw_url[8:]}')

            f = open(f'data//{raw_url[8:]}//{img[1]}.png', 'wb')
            f.write(image)
            f.close()

    # 4
    yield None, Status.CLOSE
    yield None, Status.CLOSE
