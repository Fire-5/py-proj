import socket as sockets
import select
import time



class Server(object):
    # List to keep track of socket descriptors
    CONNECTION_LIST = {}
    # {SOCKET : NAME}
    RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2
    PORT = 5000

    inputs = []                     # сокеты, которые будем читать
    outputs = []                    # сокеты, в которые надо писать
    excepts = []                    # сокеты, которые надо закрыть

    def __init__(self):
        print("... Init...")
        self.server_socket = sockets.socket(sockets.AF_INET,
                                            sockets.SOCK_STREAM)
        self.set_up_connections()
        self.client_connect()

    def set_up_connections(self):
        print("... Setup...")
        # this has no effect, why ?
        self.server_socket.setsockopt(sockets.SOL_SOCKET,
                                       sockets.SO_REUSEADDR, 1)
        self.server_socket.bind(("127.0.0.1", self.PORT))
        self.server_socket.listen(10)  # max simultaneous connections.

        # Add server socket to the list of readable connections
        self.CONNECTION_LIST[self.server_socket] = 'SERVER'

    def setup_connection(self):
        print("... Connection...")
        sockfd, addr = self.server_socket.accept()
        sockfd.setblocking(0)

        print("... Setup client ...")
        self.send_data_to(sockfd, "please enter a username: ")
        name = self.listen_data_to(sockfd)
        self.CONNECTION_LIST[sockfd] = name

        print("Client {} connected".format(name))
        self.broadcast_message(sockfd, "Client {} connected".format(name))
        return sockfd

    def listen_data_to(self, sock):
        text = ''
        try:
            data = sock.recv(self.RECV_BUFFER)
            text = data.decode()
            return text
        except:
            print(' >>> NO DATA <<<')
            return ''


    def send_data_to(self, sock, message):
        # print("... Send to {}: {}...".format(sock.getsockname(), message))
        try:
            sock.send(message.encode('utf-8'))
            self.outputs.append(sock)
        except Exception as e:
            print(e)
            # broken socket connection may be,
            # chat client pressed ctrl+c for example
            # print("Client {} not responseble".format(sock.getsockname()))
            self.excepts.append(sock)

    # Function to broadcast chat messages to all connected clients
    def broadcast_message(self, sock, message):
        for socket in self.CONNECTION_LIST:
            if socket != self.server_socket and socket != sock:
                # socket.send(message.encode('utf-8'))
                self.send_data_to(socket, message)


    def client_connect(self):
        self.inputs.append(self.server_socket)

        print("Chat server started on port " + str(self.PORT))
        message = ''
        while True:
            self.reads, self.send, self.excepts = select.select(self.inputs, self.outputs, self.excepts)
            local_time = time.ctime(time.time())
            print(local_time,
                  len(self.inputs),
                  len(self.outputs),
                  len(message),
                  end = ' ')


            for sock in self.reads:
                if sock == self.server_socket:
                    new_conn = self.setup_connection()
                    self.inputs.append(new_conn)

                else:
                    data = self.listen_data_to(sock)
                    if data != '':
                        name = self.CONNECTION_LIST[sock]
                        message = name + '> ' + data + '\n'
                        print(' > ' + name + ': ' + message)
                        # if sock not in self.outputs:
                        #     self.outputs.append(sock)

                    else:
                        self.excepts.append(sock)

                self.broadcast_message(sock, message)
                message = ''

            for sock in self.send:
                self.outputs.remove(sock)

            for sock in self.excepts:
                print("... Client {} disconnected".format(sock.getsockname()))
                self.broadcast_message(sock, "Client {} disconnected".format(sock.getsockname()))
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