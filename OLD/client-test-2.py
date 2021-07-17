import socket
import select
import sys
import time
import msvcrt
import signal
import pickle
import struct
import argparse

def prompt():
    print(' > ')
    # sys.stdout.write("> ")
    # sys.stdout.flush()



class Client(object):

    inputs = []                     # сокеты, которые будем читать
    outputs = []                    # сокеты, в которые надо писать
    excepts = []                    # сокеты, которые надо закрыть

    def __init__(self):

        # self.host = sys.argv[1]
        # self.port = int(sys.argv[2])
        self.host = "127.0.0.1"
        self.port = 5000
        self.connected = True

        print('... SETUP ...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setblocking(0)
        # sock.settimeout(16)
        try:
            self.sock.connect((self.host, self.port))

            login = self.sock.recv(1024)
            print(' > Service:', login.decode())
            self.name = input('My name is ')
            self.sock.send(self.name.encode('utf-8'))

            print('... Connected ...')
            self.inputs.append(self.sock)
            self.wait_for_messages()

        except Exception as e:
            print(e)
            sys.exit()

    def listen_data_to(self, sock):
        text = ''
        while True:
            try:
                data = sock.recv(2048)
                text = text + data.decode() + '\n'
                return text
            except Exception as e:
                print(e)
                print(' >>> NO DATA <<<')
                return ''

    def wait_for_messages(self):
        ST_TIME = time.time()
        while True:
            message = ''
            self.reads, self.send, self.excepts = select.select(self.inputs, self.outputs, self.excepts)

            print(len(self.outputs), len(self.inputs), len(message))
            local_time = time.ctime(time.time())

            for sock in self.reads:
                message = self.listen_data_to(sock)
                print('>', message)
                self.outputs.append(sock)

            # Пробежка по сокетам, готовым к отправке сообщений
            for sock in self.send:
                try:
                    mess = 'Test'
                    # mess = input(' > ')
                    # time.sleep(1)
                    sock.send(mess.encode('utf-8'))
                    # self.outputs.remove(sock)
                except:
                    continue

            for sock in self.excepts:
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