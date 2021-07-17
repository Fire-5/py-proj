# -*- coding: utf-8 -*-

import select
from socket import socket, AF_INET, SOCK_STREAM

# чтение клиентских запросов
def clients_read(r_clients, clientlist):
    responses = {} # Словарь ответов сервера вида {сокет: запрос}
    #for sock in clients:
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            responses[sock] = data
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(),
                                                   sock.getpeername()))
            clientlist.remove(sock)
            return responses

# ответы клиентам на их запросы
def clients_write(requests, w_clients, all_clients):
    for sock in w_clients:
        if sock in requests:
            try: # Подготовить и отправить ответ сервера
                response = requests[sock].encode('utf-8')
                sock.send(response.lower())
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(),
                                                       sock.getpeername()))
                sock.close()
                all_clients.remove(sock)

def mainserver():
    print('Server is START')
    address = ('localhost', 8888)
    clients = []
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2) # Таймаут для операций с сокетом
    while True:
        try:
            conn, addr = s.accept() # Проверка подключений
        except OSError as e:
            pass # timeout вышел
        else:
            print('Получен запрос на соединение от ',str(addr))
            clients.append(conn)
        finally: # Проверить наличие событий ввода-вывода
            wait = 10
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass # Ничего не делать
            requests = clients_read(r, clients)
            if requests:
                clients_write(requests, w, clients)
    print('Server is RUN')

mainserver()