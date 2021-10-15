import socket
import os
import request


class Status(enum.Enum):
	START = enum.auto()
	GET   = enum.auto()
	ERROR = enum.auto()
	CLOSE = enum.auto()


def setup_url(raw_url):
	print(f'[T] {raw_url}')
	if 'https://' in raw_url:
		PORT = 433
		task_url = raw_url[8:]

	elif 'http://' in raw_url:
		PORT = 80
		task_url = raw_url[7:]

	try:
		HOST = socket.gethostbyname(task_url)

	except Exception as e:
		HOST = None
		print(f'[ERROR] check site access {task_url}\n ---> {e}')
	
	finally:
		return HOST, PORT

def setup_socket(url, port):
	_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		_socket.connect((HOST, PORT))
		return socket

	except Exception as e:
		print(f'[ERROR] Error connect to {task_url}\n ---> {e}')
		return None

def request_get():
	request = b''
	return request

def request_img(raw_url):
	r = requests.Request('GET', task_url)
	req = r.prepare()
	# https://httpbin.org/image/png
	request = f'GET {req.path_url} HTTP/1.1\r\nHOST: {task_url}\r\n\r\n'
	request = request.encode('utf-8')
	return request

def Generator_url(raw_url):
	# 0
	# host, port = setup_url(raw_url)
	# socket = setup_socket(host, port)
	socket = 1
	# 1
	yield socket, Status.START

	request = '2'
	# 2
	yield request, Status.GET

	# 3
	raw_data = yield

	print(raw_data)
	# 4
	# создать генераторы имг

	# 5
	yield None, Status.CLOSE

def Generator_img(img_url, src_name):
	# 0

	# 1
	yield socket, Status.START

	# 2
	request = ''
	yield request, Status.GET

	raw_data = yield

	headers = raw_data.split(b'\r\n\r\n')[0]
	image   = raw_data[len(headers)+4:]

	f = open(f'{img_url}/{src_name}++.png', 'wb')
	f.write(image)
	f.close()
	# 3
	yield None, Status.CLOSE