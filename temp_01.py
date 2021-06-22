# -*- coding: utf-8 -*-

'''
Запрос:
GET /index.php HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9b5) Gecko/2008050509 Firefox/3.0b5
Accept: text/html
Connection: close

# Ошибка 497 на некоторых сайтах - это значит, что меня не пускает
# фаерволл сервиса, к которому я подключаюсь. Пробовал Ситилинк,
# ДНС, М.Видео...
# Яндекс же наоборот нормально все отдает, но кол-во контента,
# которое он отдает - это просто жесть. Программа вылетает с ошибкой
# декодинга какого то байта в поступающих данных. Это в части ответа
# Message Body от Сервера.

'''

import asyncio
import aiohttp
import socket
import time

start = time.time() # Время начала отсчета

urls = [
    ['http://www.google.com', '172.217.18.110', 80],
    ['http://www.yandex.ru', '77.88.55.55'   , 80],
    ['http://www.python.org', '138.197.63.241', 80],
    ['http://vk.com', '87.240.190.67', 80],
    ['http://www.youtube.com', '142.250.181.238', 80],
    ['http://mail.ru', '94.100.180.201', 80]
]



# Функция измерения времени
def tic():
    return 'at %1.3f seconds' % (time.time() - start)

async def send(socket, addres, request):
    # Подключаемся по заранее указанному адресу
    socket.connect(addres)
    # Передаем HTTP Запрос.
    socket.send(request)
    print('... Done')


async def listen(socket):
    data = ''
    while True:
        # Получаем информацию по 1024 байта
        in_data = socket.recv(1024)
        data = data + in_data.decode()
        if not in_data:
            break # Если данных нет, то выходим из цикла
    # Закрываем соединение.
    socket.close()
    return data

async def call_url_socet(url):
    print('Starting ', url[0], end='')
    # Создаем объект сокета для подключения
    connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (url[1],url[2])
    req = 'GET / HTTP/1.1\nHost: {}\nContent-Type: text/html\nConnection: close\n\n'.format(url[0]).encode()
    await send(connect_socket, addr, req)

    data = await listen(connect_socket)
    print(' ---- ', tic(), url[0], 'bytes:', len(data), data[:50], '\n')
    return data


async def call_url(url):
    print('Starting ', url[0])
    try:
        # Асинхронный запрос 'GET' к сайту по url представить как "запрос"
        async with aiohttp.request('GET', url[0]) as response:
        #response = await aiohttp.get(url) # Не работает на py3.6
            # Получаем данные в виде текста
            st = await response.status
            data = await response.text()
            # Выводим результат получения данных
            print('{}:{}: status: {} bytes: {} '.format(tic(),
                                                        url[0],
                                                        st,
                                                        len(data)))

    except:
        print(' >>>> {} is unresponsive'.format(url[0]))
    response.close()


# Создание главного цикла
loop = asyncio.get_event_loop()

futures1 = [call_url(url) for url in urls]
futures2 = [call_url_socet(url) for url in urls]
# Запуск в цикле асихронных функций
loop.run_until_complete(asyncio.wait(futures1))
loop.run_until_complete(asyncio.wait(futures2))
# Как только закончатся выполнения функций, закрыть цикл
loop.close()

print('\n\n\n\n\n >>> Done <<<')