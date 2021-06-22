# -*- coding: utf-8 -*-

##########################################################
'''
Пример по асинхронному запросу к сайтам и получению от них данных.
Градация делается с учетом времни запроса.
'''

# import time
# import asyncio
# import aiohttp

# # Список сайтов для опроса
# urls = [
#     'http://www.google.com',
#     'http://www.yandex.ru',
#     'http://www.python.org',
#     'https://vk.com/',
#     'https://www.youtube.com/',
#     'https://mail.ru/',
#     'http://tapochek.net/index.php'
# ]
# start = time.time() # Время начала отсчета

# # Функция измерения времени
# def tic():
#     return 'at %1.3f seconds' % (time.time() - start)

# # Асинхронная функция для опроса сайта по url
# async def call_url(url):
#     print('Starting {}'.format(url))
#     # Асинхронный запрос 'GET' к сайту по url представить как "запрос"
#     async with aiohttp.request('GET', url) as response:
#     #response = await aiohttp.get(url) # Не работает на py3.6
#         # Получаем данные в виде текста
#         data = await response.text()
#         # Выводим результат получения данных
#         #print('>>>> {}:{}: {} bytes: {}'.format(tic(), url, len(data), 'data'))
#         print(tic(), url, 'bytes:', len(data), 'data')
#         return data

# #Футура - объект с результатом выполнеиня задачи.
# futures = [call_url(url) for url in urls]

# # Создание главного цикла
# loop = asyncio.get_event_loop()
# # Запуск в цикле асихронных функций
# loop.run_until_complete(asyncio.wait(futures))
# # Как только закончатся выполнения функций, закрыть цикл
# loop.close()

##########################################################
'''
Пример с блокировкой некоторых задач, пока выполняется другая задача.
Распределение идет через распределение приоритерта между задачами.
'''

#import time
#import asyncio
##import nest_asyncio
#
##nest_asyncio.apply()    # Модуль для обхода выполнениея цикла в цикле...
#start = time.time()     # Время начала отсчета
#
## Функция измерения времени
#def tic():
#    return 'at %1.4f seconds' % (time.time() - start)
#
#
#async def gr1():
#    # Задача 1.
#    print('gr1 started work: {}'.format(tic()))
#    # Можно прерваться и передать управление дальше.
#    # В скобочках устанавливается приоритет задачи.
#    await asyncio.sleep(2)
#    print('gr1 ended work: {}'.format(tic()))
#    await asyncio.sleep(2)
#
#
#async def gr2():
#    # Задача 2. Аналогичная задаче 1, но приоритет ниже.
#    print('gr2 started work: {}'.format(tic()))
#    await asyncio.sleep(3)
#    print('gr2 Ended work: {}'.format(tic()))
#    await asyncio.sleep(3)
#
#async def gr4():
#    # Задача 4. Аналогичная задаче 2.
#    print('gr4 started work: {}'.format(tic()))
#    await asyncio.sleep(3)
#    print('gr4 Ended work: {}'.format(tic()))
#    await asyncio.sleep(3)
#
#async def gr5():
#    # Задача 5. Аналогичная задаче 2.
#    print('gr5 started work: {}'.format(tic()))
#    await asyncio.sleep(3)
#    print('gr5 Ended work: {}'.format(tic()))
#    await asyncio.sleep(3)
#
#
#async def gr3():
#    # Задача 3.
#    print("Let's do some stuff while the coroutines are blocked: {}".format(tic()))
#    # Выполнение может прерваться, но приорет выставлен 1, т.е. выше остальных.
#    await asyncio.sleep(1)
#    print("Done!: {}".format(tic()))
#    await asyncio.sleep(1)
#
## Создание главного цикла.
#loop = asyncio.get_event_loop()
## Создание списка задач (порядок имеет значение только на порядок старта задач).
#tasks = [
#    loop.create_task(gr1()),
#    loop.create_task(gr2()),
#    loop.create_task(gr3()),
#    loop.create_task(gr4()),
#    loop.create_task(gr5())
#]
## Запуск в цикле асихронных функций
#loop.run_until_complete(asyncio.wait(tasks))
## Как только закончатся выполнения функций, закрыть цикл
#loop.close()

##########################################################
'''
Опрос сайтов, которые показывают мой IP. При этом не ожидаем ответы всех сайтов,
а прекращаем программу после ответа хотя бы одного из таких сервисов.

...Когда футура находится в состояние done, у неё можно получить результат
выполнения. В состояниях pending и running такая операция приведёт
к исключению InvalidStateError, а в случае canelled будет CancelledError,
и наконец, если исключение произошло в самой корутине,
оно будет сгенерировано снова (также, как это сделано при вызове exception)...
'''

#from collections import namedtuple
#import time
#import asyncio
#from concurrent.futures import FIRST_COMPLETED
#import aiohttp
#
## Создаем структуру именованного списка (???)
#Service = namedtuple('Service', ('name', 'url', 'ip_attr'))
#
## Указываем сервисы для получения данных
#SERVICES = (
#    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
#    Service('ip-api', 'http://ip-api.com/json', 'query')
#)
#
## Асинхронная функция опроса сервиса
#async def fetch_ip(service):
#    start = time.time()     # Время начала опроса
#    print('Fetching IP from {}'.format(service.name))
#
#    # Асинхронный запрос 'GET' к сервису представить как "запрос"
#    #response = await aiohttp.request('GET', service.url)
#    async with aiohttp.request('GET', service.url) as response:
#        # Преобразование запроса в json
#        json_response = await response.json()
#        # Получение аттрибута со значение ip
#        ip = json_response[service.ip_attr]
#
#        # Закрытие запроса
#        response.close()
#        return '{} finished with result: {}, took: {:.2f} seconds'.format(
#            service.name, ip, time.time() - start)
#
## Создание асинхронной функции по пробегу по всем сервисам из списка
#async def asynchronous():
#    futures = [fetch_ip(service) for service in SERVICES]
#    # done - Выполнено, pending - Ожидает
#    # Выполняется до первого выполненного запроса
#    done, pending = await asyncio.wait(
#        futures, return_when=FIRST_COMPLETED)
#
#    # Вывод выполненного запроса на экран
#    print(done.pop().result())
#
#    # Закрытие остальных запросов
#    for future in pending:
#        future.cancel()
#
## Создание главного цикла
#ioloop = asyncio.get_event_loop()
## Запуск в цикле асихронных функций
#ioloop.run_until_complete(asynchronous())
## Как только закончатся выполнения функций, закрыть цикл
#ioloop.close()

##########################################################
'''
Тот же пример, только с обработчиком запросов и исключений.
Выводятся все сервисы, каждый со своим временем и одним, который без ответа.
'''

from collections import namedtuple
import time
import asyncio
import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query'),
    Service('borken', 'http://no-way-this-is-going-to-work.com/json', 'ip')
)


async def fetch_ip(service):
    start = time.time()
    print('Fetching IP from {}'.format(service.name))

    # Ставим обработчик исключений
    # Если все верно, то выполняем стандартный код
    try:
        async with aiohttp.request('GET', service.url) as response:
            json_response = await response.json()
            ip = json_response[service.ip_attr]
            return ' >>> {} finished with result: {}, time: {:.2f} seconds'.format(
                service.name, ip, time.time() - start)
    # Иначе возвращаем строку с ошибкой
    except:
        return ' >>> {} is unresponsive'.format(service.name)

    # В конце закрываем запрос.
    response.close()


async def asynchronous():
    # Пробежка по Сервисам
    futures = [fetch_ip(service) for service in SERVICES]
    done, _ = await asyncio.wait(futures)

    # Всем, кто выполнился - выписать результат
    for future in done:
        print(future.result())

# стандартный запуск
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()

##########################################################
'''
Таймауты.
'''
# import time
# import random
# import asyncio
# import aiohttp
# import argparse
# from collections import namedtuple
# from concurrent.futures import FIRST_COMPLETED

# Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

# SERVICES = (
#     Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
#     Service('ip-api', 'http://ip-api.com/json', 'query'),
#     #Service('borken', 'http://no-way-this-is-going-to-work.com/json', 'ip')
# )

# # Время на выполнение задачи.
# # Рекомендовано значение 0.5
# DEFAULT_TIMEOUT = 0.1


# async def fetch_ip(service):
#     start = time.time()
#     print('Fetching IP from {}'.format(service.name))

#     try:
#         async with aiohttp.request('GET', service.url) as response:
#             json_response = await response.json()
#             ip = json_response[service.ip_attr]
#             print('{} finished with result: {}, took: {:.2f} seconds'.format(
#                     service.name, ip, time.time() - start))
#             return ip

#     except:
#         return '{} is unresponsive'.format(service.name)

#     response.close()

# async def asynchronous(timeout):
#     # Библиотека значений для передачи в вывод.
#     resp = {
#         "message": "None",
#         "ip": "not available"
#     }

#     # Запускаем проверку сайтов по Сервисам
#     futures = [fetch_ip(service) for service in SERVICES]
#     done, pending = await asyncio.wait(
#         futures, timeout=timeout, return_when=FIRST_COMPLETED)

#     # Пробегаемся по задачам в ожидании и закрываем их (будет сообщение!)
#     for future in pending:
#         # print(">>> {} is cancel".format(futures))
#         future.cancel()
#     # Пробегаемся по выполненным задачам и получаем значение
#     for future in done:
#         resp["message"] = 'Done'
#         resp["ip"] = future.result()
#         future.cancel()

#     print(resp)

# # Создание нового аргумента для запуска файла программы. ВАЖНОЕ!
# parser = argparse.ArgumentParser()
# parser.add_argument(
#     '-t', '--timeout',
#     help='Timeout to use, defaults to {}'.format(DEFAULT_TIMEOUT),
#     default=DEFAULT_TIMEOUT, type=float)
# args = parser.parse_args()

# # Вывод основного аргумента
# print("Using a {} timeout".format(args.timeout))

# # стандартный запуск
# ioloop = asyncio.get_event_loop()
# ioloop.run_until_complete(asynchronous(args.timeout))
# #ioloop.close()
# print('')

'''
Функция map.
'''
# import urllib3

# urls = ['http://www.yahoo.com', 'http://www.reddit.com']
# results = map(urllib3.urlopen, urls)
# print(results)

'''
Небольшая программка, что бы получить список ссылок на все
файлы\странички сайта через sitemap.xml
'''

# import aiohttp
# import asyncio

# from lxml import etree


# async def fetch(session, url):
#     async with session.get(url) as response:
#         # Возвращаем ответ в байтах
#         return await response.content.read()


# async def main():
#     async with aiohttp.ClientSession() as session:
#         xml_str = await fetch(session, 'https://sdvk-oboi.ru/sitemap.xml')
#         root = etree.fromstring(xml_str)

#         for url in root.xpath('//*[local-name()="loc"]/text()'):
#             print(url)


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())