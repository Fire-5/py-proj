import socket as sockets
import select
import time
import sys

class Server(object):
    # Список подключенных клиентов
	CONNECTION_LIST = {}
    # {SOCKET : NAME}
	RECV_BUFFER = 4096
	inputs = [sys.stdin]			# сокеты, которые будем читать
	outputs = []                    # сокеты, в которые надо писать
	excepts = []                    # сокеты, которые надо закрыть

	def __init__(self):
		HOST = '127.0.0.1'
		PORT = 5000

		print('... INIT')
		self.server_socket = sockets.socket(sockets.AF_INET, sockets.SOCK_STREAM)
		self.server_socket.setsockopt(sockets.SOL_SOCKET, sockets.SO_REUSEADDR, 1)
		self.server_socket.bind((HOST, PORT))
		self.server_socket.listen()

        # Добавление сокета сервера в лист подключений с именем 'SERVER'
		self.CONNECTION_LIST[self.server_socket] = 'SERVER'
		self.inputs.append(self.server_socket)

		self.client_connect()

	def client_setup_connection(self):
        # Настройка подключения клиента.
		print("... Connection...")
        # Принятие подключения нового сокета.
		sockfd, addr = self.server_socket.accept()
		sockfd.setblocking(0)
		sockfd.settimeout(12)

		try:
			print("... Setup client ...")
            # # Настройка имени клиента
            # sockfd.send("please enter a username: ".encode('utf-8'))
            
            # data = sock.recv(self.RECV_BUFFER)
            # time.sleep(5)
            # name = data.decode()
            
			name = 'name-' + str(addr)
			self.CONNECTION_LIST[sockfd] = name
			print("Client {} connected".format(name))
			return sockfd

		except Exception as e:
			print(e)
			sys.exit()

	def broadcast_message(self, sock, message):
    # Широковещательная передача
		for socket in self.CONNECTION_LIST:
			if socket != self.server_socket and socket != sock:
				sock.send(message.encode('utf-8'))


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
			print(local_time, len(self.inputs), len(self.outputs), len(message), end = ' ')

            # Пробежка по сокетам, готовым принимать сообщения
			for sock in reads:
                # Если сокет является серверным сокетом:
                # Значит новое подключение.
				if sock == self.server_socket:
					new_conn = self.client_setup_connection()
					self.inputs.append(new_conn)

                # Иначе, это прием сообщения
				else:
					data = sock.recv(self.RECV_BUFFER)
					data = data.decode()
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
					elf.inputs.remove(sock)
				if sock in self.outputs:
					self.outputs.remove(sock)
				sock.close()

		print("... Close ...")
		self.server_socket.close()


if __name__ == "__main__":
	start = time.time()
	server = Server()