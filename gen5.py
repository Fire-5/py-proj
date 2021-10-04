import socket
import enum


class Status(enum.Enum):
	START = enum.auto()
	GET   = enum.auto()
	ERROR = enum.auto()
	CLOSE = enum.auto()


def generator(raw_url):
	# 0
	print(f'[+] Task URL: {raw_url}')

	# 1
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	yield sock, Status.START
	print(f'[+] It`s worked!')

	# 2
	msg = 'yeap'
	yield msg, Status.GET

	# 3
	raw_data = yield
	print(f'[+] Download data:\n{raw_data}')

	# 4
	yield None, Status.CLOSE