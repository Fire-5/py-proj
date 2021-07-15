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
        name = self.set_client_user_name(sockfd)
        self.CONNECTION_LIST[sockfd] = name
        print("Client {} connected".format(name))
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


    def set_client_user_name(self, sock):
        print("... Setup client ...")
        self.send_data_to(sock, "please enter a username: ")
        name = self.listen_data_to(sock)
        return name

    def send_data_to(self, sock, message):
        print("... Send to {}: {}...".format(sock.getsockname(), message))
        try:
            sock.send(message.encode('utf-8'))
            self.outputs.append(sock)
        except:
            # broken socket connection may be,
            # chat client pressed ctrl+c for example
            print("Client {} not responseble".format(sock.getsockname()))
            self.excepts.append(sock)

    # Function to broadcast chat messages to all connected clients
    def broadcast_message(self, sock, message):
        for socket in self.CONNECTION_LIST:
            if socket != self.server_socket and socket != sock:
                socket.send(message.encode('utf-8'))


    def client_connect(self):
        self.inputs.append(self.server_socket)

        print("Chat server started on port " + str(self.PORT))

        while True:
            self.reads, self.send, self.excepts = select.select(self.inputs, self.outputs, self.excepts)
            message = ''

            for sock in self.reads:
                if sock == self.server_socket:
                    new_conn = self.setup_connection()
                    # поместим новый сокет в очередь на прослушивание
                    self.inputs.append(new_conn)
                else:
                    # data = sock.recv(self.RECV_BUFFER)
                    name = self.CONNECTION_LIST[sock]
                    data = self.listen_data_to(sock)
                    message = message + name + data + '\n'


            for sock in self.send:
                if len(message):
                    # если есть сообщения - то отсылаем
                    self.broadcast_message(sock, message)
                else:
                    # если нет сообщений - удаляем из очереди
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




        #     reads, send, excepts = select.select(inputs, outputs, excepts)
        #     # список READS - сокеты, готовые к чтению
        #     for sock in reads:
        #         print("... R ...")
        #         if sock == self.server_socket:
        #             new_conn = self.setup_connection()
        #             # поместим новый сокет в очередь на прослушивание
        #             inputs.append(new_conn)
        #         else:
        #             try:
        #                 data = sock.recv(self.RECV_BUFFER)
        #                 if data:
        #                     if self.user_name_dict[sock].username is None:
        #                         self.set_client_user_name(data, sock)
        #                         outputs.append(sock)

        #             except:
        #                 addr = sock.getsockname()
        #                 self.broadcast_data(sock, "Client {} is offline".format(addr))
        #                 print("Client {} is offline".format(addr))
        #                 self.CONNECTION_LIST.remove(sock)
        #                 continue

        #     # список SEND - сокеты, готовые принять сообщение
        #     for conn in send:
        #         print("... S...")
        #         self.broadcast_data(sock, "\r" + '<' + self.user_name_dict[sock].username + '> ' + data)
        #         if sock not in inputs:
        #             inputs.append(sock)
        #         outputs.remove(conn)

        #     # список EXCEPTS - сокеты, в которых произошла ошибка
        #     for conn in excepts:
        #         print("... E...")
        #         # удаляем сокет с ошибкой из всех очередей
        #         if sock in inputs:
        #             inputs.remove(sock)
        #         if sock in outputs:
        #             outputs.remove(sock)
        #         sock.close()

        #     print(time.time() - start)
        #     time.sleep(1)
        #     if (time.time() - start) > 60:
        #         break

        # print("... Close ...")
        # self.server_socket.close()


        #     for sock in read_sockets:
        #         # New connection
        #         if sock == self.server_socket:
        #             # Handle the case in which there is
        #             # a new connection recieved through server_socket
        #             self.setup_connection()
        #         # Some incoming message from a client
        #         else:
        #             # Data recieved from client, process it
        #             try:
        #                 data = sock.recv(self.RECV_BUFFER)
        #                 if data:
        #                     if self.user_name_dict[sock].username is None:
        #                         self.set_client_user_name(data, sock)
        #                     else:
        #                         self.broadcast_data(sock, "\r" + '<' + self.user_name_dict[sock].username + '> ' + data)

        #             except:
        #                 addr = sock.getaddrinfo
        #                 self.broadcast_data(sock, "Client {} is offline".format(addr))
        #                 print("Client {} is offline".format(addr))
        #                 sock.close()
        #                 self.CONNECTION_LIST.remove(sock)
        #                 continue
        # self.server_socket.close()




class Connection(object):
    def __init__(self, address):
        self.address = address
        self.username = None


if __name__ == "__main__":
    start = time.time()
    server = Server()