import socket
import select
import sys
import time


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
        # self.sock = None
        self.connect_socket()


    def connect_socket(self):
        print('... SETUP ...')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            # self.sock.settimeout(16)
            try:
                sock.connect((self.host, self.port))
                print('Connected to remote host. Start sending messages')
                self.inputs.append(sock)
                self.outputs.append(sock)
                self.wait_for_messages()
            except Exception as e:
                print(e)
                sys.exit()

    def wait_for_messages(self):
        while True:
            self.reads, self.send, self.excepts = select.select(self.inputs, self.outputs, self.excepts)
            print(len(self.outputs), len(self.inputs))

            for sock in self.reads:
                local_time = time.ctime(time.time())
                data = sock.recv(4096)
                message = data.decode()
                print(local_time, '>', message)


            for sock in self.send:
                local_time = time.ctime(time.time())
                mess = input(' > ')
                sock.send(mess.encode('utf-8'))

            for sock in self.excepts:
                local_time = time.ctime(time.time())
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