import socket
import select
import gen3

def listen_data(sock):
    ''' метод приема данных и формирование их в массив данных'''
    data = ''
    while True:
        raw = sock.recv(128)
        try:
            data += raw.decode('utf-8')
            if len(raw) == 0:
                break

        except UnicodeDecodeError as e:
            print('[!] Unicode Error!\n{e}')
            continue
    return data

Status = gen3.Status
urls1 = ['http://www.python.org']
urls2 = [
    'http://www.google.com',
    'http://www.yandex.ru',
    'http://www.python.org',
    'https://vk.com',
    'https://www.youtube.com',
    'http://tapochek.net'
]

generators = map(gen3.generator, urls1)    # Вариант 1
# generators = map(gen3.generator, urls2)   # Вариант 2
tasks = {}

inputs = []
outputs = []
errors = []

for task in generators:
	# 0
	sock, st = next(task)
	print(f'[+] {st} ')
	if st != Status.START:
		print("[ERROR] Task error in step 1")
		task.close()

	else:
		tasks[sock] = task
		outputs.append(sock)

print(len(tasks))

while True:
	try:
		rsock, wsock, ersock = select.select(inputs, outputs, errors)
	print(len(rsock), len(wsock), len(ersock))

	for sock in wsock:
		# 1
		msg, st = next(tasks[sock])
		if st == Status.GET:
			sock.send(msg)
			inputs.append(sock)
			outputs.remove(sock)

		if st == Status.LOAD:
			sock.send(msg)
			print('[+] GOOD')
			inputs.append(sock)
			outputs.remove(sock)

		if st == Status.ERROR or st == Status.CLOSE:
			ersock.append(sock)

	for sock in rsock:
		data = listen_data(sock)
		# 2
		tasks[sock].send(data)
		outputs.append(sock)
		inputs.remove(sock)

	for sock in ersock:
		# удаление сокета.
		print('[-] Task close')
		try:
			outputs.remove(sock)
		except:
			continue

		tasks[sock].close()
		sock.close()
		break

print('[!] Quit')