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
from lxml import etree

start = time.time() # Время начала отсчета

# urls = [
#     ['https://www.google.com/', '172.217.18.110', 443],
#     ['https://yandex.ru/', '77.88.55.66'   , 443],
#     ['https://www.python.org/', '138.197.63.241', 443],
#     ['https://vk.com/', '87.240.190.67', 443],
#     ['https://www.youtube.com/', '142.250.181.238', 443],
#     ['https://mail.ru/', '94.100.180.201', 443]
# ]

urls = []
file_urls = open('urls.txt')

for line in file_urls:
    line = line.replace('\n', '')
    nline = line.replace('https://', '')
    nline = nline.replace('http://', '')
    nline = nline.replace('www.', '')[:-1]
    ip = socket.gethostbyname_ex(nline)
    urls.append(ip)
print(urls)


# Функция измерения времени
def tic():
    return 'at %1.3f seconds' % (time.time() - start)

#####################################################

async def send(socket, url):
    req = 'GET /index.php HTTP/1.1\nHost: {}\nContent-Type: text/html\nConnection: close\n\n'.format(url[0]).encode()
    # Подключаемся по заранее указанному адресу
    addres = (url[2][0],433)
    socket.connect(addres)
    # Передаем HTTP Запрос.
    socket.send(req)
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

    await send(connect_socket, url)

    data = await listen(connect_socket)
    print(' ---- ', tic(), url[0], 'bytes:', len(data), data[:50], '\n')
    return data

#####################################################

# async def call_sitemap(url):
#      async with aiohttp.request('GET', 'https://'+url[0]+'/sitemap.xml') as response:
#         st = response.status
#         data = await response.content.read()
#         # Выводим результат получения данных
#         print('SITEMAP: {}:  STATUS: {}    bytes: {} '.format(url[0],st, len(data)))
#         if st==200:
#             # Асинхронная задержка, что бы все результаты отписались,
#             # а потом уже выводить содержание ответа.
#             await asyncio.sleep(2)
#             # Небольная проверка того, что возвращается с сообщением.
#             # print("##################################################")
#             print(' --->', url[0])
#             # print(data)
#             # print("##################################################\n\n")
#             try:
#                 root = etree.fromstring(data)
#                 for url in root.xpath('//*[local-name()="loc"]/text()'):
#                     print(url)
#             except:
#                 print('Error in sitemap.xml!!!')
#             print()
#         else:
#             print(' Bad request!!!')

# async def call_url(url):
#     print('Starting ', url[0])
#     # Асинхронный запрос 'GET' к сайту по url представить как "запрос"
#     async with aiohttp.request('GET', 'https://'+url[0]) as response:
#     #response = await aiohttp.get(url) # Не работает на py3.6
#         # Получаем данные в виде текста
#         st = response.status
#         data = await response.content.read()
#         # Выводим результат получения данных
#         print('GET: {}:{}:  STATUS: {}  bytes: {}'.format(tic(), url[0],st, len(data)))
#         if st==200:
#             print(' Good request')
#             await call_sitemap(url)
#         else:
#             print(' Bad request!!!')



#     response.close()

#####################################################

# Создание главного цикла
loop = asyncio.get_event_loop()
'''
Фютуры1 - это запросы сайтов через библиотеку aiohttp. Работают.
Если запрос хорошоший на sitemap.xml, то еще и есть вывод HTML-странички в STDOUT.

Футуры2 - это запросы сайтов через собственные конструкции сокетов. К сожалению все выдают ошибку 400 "Bad Request". Не знаю в чем проблема и
где искать причину...

После идут два цикла loop с запусками их.
'''
# futures1 = [call_url(url) for url in urls]
futures2 = [call_url_socet(url) for url in urls]
# Запуск в цикле асихронных функций
# loop.run_until_complete(asyncio.wait(futures1))
loop.run_until_complete(asyncio.wait(futures2))
# Как только закончатся выполнения функций, закрыть цикл
loop.close()

print('\n >>> Done <<<')