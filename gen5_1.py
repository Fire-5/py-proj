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
    END = enum.auto()
    APPEND_1 = enum.auto()
    APPEND_2 = enum.auto()


def setup_generator(generators_list):
    """Функция, которая подготавливает (делает первый шаг)
    в списке генераторов. На вход требует список генераторов.
    На выход выдает пару: список сокетов и словарь генератор : сокет"""

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

    raw_data = raw_data.decode('utf-8') #########
    data = raw_data.split('\r\n\r\n')[1]
    img_list = []
    soup = bs(data, 'html.parser')

    for tag in soup.find_all("img"):
        print(f" ---> {tag}")
        # img_list.append([tag])

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
Accept: text/html\r\n
Accept-Encoding: gzip, deflate\r\n
Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7\r\n
Cache-Control: max-age=0\r\n
Connection: keep-alive\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36\r\n
\r\n\r\n"""
    message = request.encode('utf-8')

    return message


def setup_url(raw_url):
    """Функция, которая по ссылке создает подключение 
    к ресурсу и возвращает готовую пару сокет-статус"""

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

def generator_img(raw_url):
    """Генератор для выкачки изображений. 
    На вход дается прямая ссылка"""

    # 0 Запуск
    print(f'[+] Task URL: {raw_url}')

    # 1 Подготовка соединения
    sock, st = setup_url(raw_url)
    yield sock, st
    print(f'[+] Step 1: Connect done!')

    # 2 Формирование запроса
    msg = request(raw_url)
    print(f'[+] Step 2: Message send!')
    yield msg, Status.GET

    # 3 Получение ответа
    image = yield None, Status.READY
    print(f'[+] Download data:\n{image[:16]}')

    # 4 Сохранениие изображения
    if not os.path.exists(f'data//{raw_url[8:]}'):
        os.mkdir(f'data//{raw_url[8:]}')

    f = open(f'data//{raw_url[8:]}//{img[1]}.png', 'wb')
    f.write(image)
    f.close()

    # 5 Закрытие
    print(f'[+] Task {raw_url} finished!')
    yield None, Status.CLOSE
    yield None, Status.CLOSE


def generator(raw_url):
    """Генератор, который парсит страницу 
    и находит все ссылки на картинки.
    На вход подается прямая ссылка на ресурс"""

    # 0 Запуск
    print(f'[+] Task URL: {raw_url}')

    # 1 Подготовка соединеия
    sock, st = setup_url(raw_url)
    yield sock, st
    print(f'[+] Step 1: Connect done!')

    # 2 Формирование запроса
    msg = request(raw_url)
    print(f'[+] Step 2: Message send!')
    yield msg, Status.GET

    # 3 Получение данных и парсинг
    raw_data = yield None, Status.READY
    print(f'[+] Download data:\n{raw_data[:16]}')
    img_list = parser(raw_url, raw_data)

    # 4 Формирование новых списков задач и списка сокетов.
    if len(img_list) > 0:
        generators = map(generator_img, img_list)
        outputs, tasks = setup_generator(generators)
        
        yield outputs, Status.APPEND_1
        yield tasks, Status.APPEND_2

        yield None, Status.END


    # 5 Закрытие
    print(f'[+] Task {raw_url} finished!')
    yield None, Status.CLOSE
    yield None, Status.CLOSE
