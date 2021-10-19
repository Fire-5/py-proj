import socket
import enum
import os
import time

import requests as requests
from bs4 import BeautifulSoup as bs


class Status(enum.Enum):
    START = enum.auto()
    GET = enum.auto()
    ERROR = enum.auto()
    CLOSE = enum.auto()
    READY = enum.auto()
    LOAD = enum.auto()
    WAIT = enum.auto()
    APPEND = enum.auto()


def setup_generator(generators_list):
    """Функция, которая подготавливает (делает первый шаг)
    в списке генераторов. На вход требует список генераторов.
    На выход выдает пару: список сокетов и словарь (генератор : сокет)"""

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
    """Функция, которая разбирает входящий HTTP запрос
    и выбирает в нем все ссылки на картинки. 
    Функция возвращает массив ссылок[0] и их ID[1]"""

    raw_data = raw_data.decode('utf-8')
    data = raw_data.split('\r\n\r\n')[1]
    img_list = []
    soup = bs(data, 'html.parser')

    for tag in soup.find_all("img"):
        # print(f" ---> {url + tag.get('src')}\n ---> {tag.get('id')}")
        src = url + tag.get('src')
        img_list.append([src, tag.get('id')])

    return img_list


def request(task_url):
    """Функция, которая собирает HTTP-запрос GET
    из строки. В целом работает, но большинство сайтов видят
    этот вариант ошибочным (код ошибки 400)"""

    r = requests.Request('GET', task_url)
    req = r.prepare()
    url = task_url.replace(req.path_url, '')
    url = url.replace('https://', '')
    url = url.replace('http://', '')

    request = f"""GET {req.path_url} HTTP/1.1\r\n
HOST: {url}\r\n
Connection: keep-alive\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36\r\n
\r\n\r\n"""
    message = request.encode('utf-8')

    return message


def setup_url(raw_url):
    """Функция, которая по ссылке создает подключение 
    к ресурсу и возвращает готовую пару сокет-статус."""

    if 'https://' in raw_url:
        PORT = 433
        task_url = raw_url[8:]
    elif 'http://' in raw_url:
        PORT = 80
        task_url = raw_url[7:]

    service = task_url.split('/')[0]

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    st = Status.START
    try:
        # HOST = socket.gethostbyname(task_url)
        print(f'[T] Connect to: {service}:{PORT}')
        _socket.connect((service, PORT))
        st = Status.START

    except Exception as _exc1:
        print(f' ---> [ERROR] Error connect to {task_url}\n{_exc1}')
        st = Status.ERROR

    finally:
        return _socket, st

def generator_img(img_url):
    """Генератор для выкачки изображений. 
    На вход дается прямая ссылка"""

    # 0 Запуск
    raw_url = img_url[0]
    img_name = img_url[1]
    format = raw_url.split('.')[-1]
    directory = raw_url.split('.')[1]
    
    # 1 Подготовка соединения
    sock, st = setup_url(raw_url)
    yield sock, st

    # 2 Формирование запроса
    msg = request(raw_url)
    yield msg, Status.GET

    # 3 Получение ответа
    image = yield None, Status.READY
    if image == b'NOT IMAGE':
        print(f'[+] NOT IMAGE!!!')
        yield None, Status.ERROR

    else:
        # 4 Сохранениие изображения
        image = image.split(b'\r\n\r\n')

        if not os.path.exists(f'data//{directory}'):
            os.mkdir(f'data//{directory}')

        f = open(f'data//{directory}//{img_name}.{format}', 'wb')
        f.write(image[1])
        f.close()
        print(f'[+] File save: data//{directory}//{img_name}.{format}')

        # 5 Закрытие
        print(f'[+] Task {raw_url} finished!')
    yield None, Status.CLOSE
    yield None, Status.CLOSE


def generator(raw_url):
    """Генератор, который парсит страницу 
    и находит все ссылки на картинки.
    На вход подается прямая ссылка на ресурс"""

    # 1 Подготовка соединеия
    sock, st = setup_url(raw_url)
    yield sock, st
    # print(f'[+] Task URL: {raw_url} Step 1: Connect done!')

    # 2 Формирование запроса
    msg = request(raw_url)
    # print(f'[+] Task URL: {raw_url} Step 2: Message send!')
    yield msg, Status.GET

    # 3 Получение данных и парсинг
    raw_data = yield None, Status.READY
    # print(f'[+] Task URL: {raw_url} Download data:\n{raw_data[:16]}')
    img_list = parser(raw_url, raw_data)

    # 4 Формирование новых списков задач и списка сокетов.
    outputs = []
    tasks = []

    if len(img_list) > 0:
        generators = map(generator_img, img_list)
        outputs, tasks = setup_generator(generators)

    # time.sleep(6)
    yield None, Status.WAIT
    yield [outputs, tasks], Status.APPEND

    # print(f'[+] Task URL: {raw_url} Step 4')
    # yield None, Status.END

    # 5 Закрытие
    print(f'[+] Task URL: {raw_url} finished!')
    yield None, Status.CLOSE
    yield None, Status.CLOSE
