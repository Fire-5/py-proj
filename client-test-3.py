# -*- coding: utf-8 -*-
import socket as sockets
import select
import time
import sys

class Client(object):

    inputs = []                     # сокеты, которые будем читать
    outputs = []                    # сокеты, в которые надо писать
    excepts = []                    # сокеты, которые надо закрыть

    def __init__(self):
        # self.host = sys.argv[1]       # поля для запуска с аргументами (ip)
        # self.port = int(sys.argv[2])  # поля для запуска с аргументами (port)
        host = "127.0.0.1"
        RECV_BUFFER = 4096  # Размер буфера
        port = 5000
        connected = True

        print('... SETUP ...')
        #
        self.sock = sockets.socket(sockets.AF_INET, sockets.SOCK_STREAM)
        try:
            #
            self.sock.connect((host, port))

            #
            login = self.sock.recv(1024)
            print(' > Service:', login.decode())
            #
            self.name = input('My name is ')
            #
            self.sock.send(self.name.encode('utf-8'))

            print('... Connected ...')
            self.inputs.append(self.sock)
            self.outputs.append(self.sock)
            self.wait_for_messages()

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

    def wait_for_messages(self):
    #
        while True:
            message = ''
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
                message = self.listen_data_to(sock)
                print('>', message)


            # Пробежка по сокетам, готовым к отправке сообщений
            for sock in send:

                mess = 'Test'
                # mess = input(' > ')
                time.sleep(1)
                self.send_data_to(sock, mess)

                # self.outputs.remove(sock)


            # Пробежка по сокетам с ошибкой
            for sock in excepts:
                print(local_time, '... Disconnect ...')
                # удаляем сокет с ошибкой из всех очередей
                if sock in self.inputs:
                    self.inputs.remove(sock)
                if sock in self.outputs:
                    self.outputs.remove(sock)
                self.excepts.remove(sock)
                sock.close()
                break

        print('... QUIT ...')


if __name__ == '__main__':
    client = Client()