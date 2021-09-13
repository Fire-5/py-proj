#!python3.6
# -*- coding: utf-8 -*-
import socket as sockets
import select
import time
import sys

class Server(object):
    # Список подключенных клиентов
    CONNECTION_LIST = {}
    # {SOCKET : NAME}
    RECV_BUFFER = 4096  # Размер буфера
    PORT = 5000

    inputs = []                     # сокеты, которые будем читать
    outputs = []                    # сокеты, в которые надо писать
    excepts = []                    # сокеты, которые надо закрыть

    def __init__(self):
        # Создание и подключение функций
        print("... INIT ...")

        self.set_up_connections()
        self.client_connect()

    def set_up_connections(self):
        # Настройка сокета
        print("... Setup...")
        self.server_socket = sockets.socket(sockets.AF_INET,
                                            sockets.SOCK_STREAM)
        self.server_socket.setsockopt(sockets.SOL_SOCKET,
                                       sockets.SO_REUSEADDR, 1)
        self.server_socket.bind(("127.0.0.1", self.PORT))
        self.server_socket.listen()
        self.inputs.append(self.server_socket)
        # Добавление сокета сервера в лист подключений с именем 'SERVER'
        self.CONNECTION_LIST[self.server_socket] = 'SERVER'

    def client_setup_connection(self):
        # Настройка подключения клиента.
        print("... Connection...")
        # Принятие подключения нового сокета.
        sockfd, addr = self.server_socket.accept()
        sockfd.setblocking(0)
        sockfd.settimeout(12)

        try:
            print("... Setup client ...")
            # Настройка имени клиента
            self.send_data_to(sockfd, "please enter a username: ")
            name = self.listen_data_to(sockfd)
            while not len(name):
                self.CONNECTION_LIST[sockfd] = name
            print("Client {} connected".format(name))
            return sockfd

        except Exception as e:
            print(e)
            sys.exit()

    def listen_data_to(self, sock):
        # Получение данных от клиента
        text = ''
        try:
            data = sock.recv(self.RECV_BUFFER)
            text = data.decode()
            return text
        except:
            print(' >>> NO DATA <<<')
            return ''

    def send_data_to(self, sock, message):
        # Отправка данных клиенту
        try:
            sock.send(message.encode('utf-8'))
        except Exception as e:
            print('... Can`t send messages ...')
            print(e)
            self.excepts.append(sock)

    def broadcast_message(self, sock, message):
    # Широковещательная передача
        for socket in self.CONNECTION_LIST:
            if socket != self.server_socket and socket != sock:
                self.send_data_to(socket, message)


    def client_connect(self):
        # Основной цикл работы сервера.
        print('... START ...')
        message = ''

        while True:
            # Селект-запросы
            reads, send, excepts = select.select(self.inputs,
                                                 self.outputs,
                                                 self.excepts)

            # Обновление локального времени
            local_time = time.ctime(time.time())
            # Проверка
            print(local_time,
                  len(self.inputs),
                  len(self.outputs),
                  len(message),
                  end = ' ')

            # Пробежка по сокетам, готовым принимать сообщения
            for sock in reads:
                # Если сокет является серверным сокетом:
                # Значит новое подключение.
                if sock == self.server_socket:
                    new_conn = self.client_setup_connection()
                    self.inputs.append(new_conn)

                # Иначе, это прием сообщения
                else:
                    data = self.listen_data_to(sock)
                    # Если сообщение пришло:
                    # Узнаем от кого было сообещние и делаем рассылку
                    if data != '':
                        name = self.CONNECTION_LIST[sock]
                        message = name + '> ' + data + '\n'
                        print(' > ' + message)
                        self.broadcast_message(sock, message)
                        message = ''


            # # Пробежка по сокетам, готовым к отправке сообщений
            # for sock in send:
            #     self.outputs.remove(sock)

            # Пробежка по сокетам с ошибкой
            for sock in excepts:
                print("... Client {} disconnected".format(sock.getsockname()))
                # удаляем сокет с ошибкой из всех очередей
                if sock in self.inputs:
                    self.inputs.remove(sock)
                if sock in self.outputs:
                    self.outputs.remove(sock)
                sock.close()

        print("... Close ...")
        self.server_socket.close()


if __name__ == "__main__":
    start = time.time()
    server = Server()