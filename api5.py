import select
import gen5


Status = gen5.Status
urls1 = ['http://www.google.com']
urls2 = [
    'http://www.google.com',
    'http://www.yandex.ru',
    'http://www.python.org',
    'https://vk.com',
    'https://www.youtube.com',
    'http://tapochek.net'
]

# generators = map(gen5.generator, urls1)    # Вариант 1
generators = map(gen5.generator, urls2)   # Вариант 2
tasks = {}

inputs = []
outputs = []
errors = []

for task in generators:
	# 1
	sock, st = next(task)

	if st != Status.START:
		print(f"[ERROR] Status: {st}\nTask error in step 1")
		task.close()

	else:
		tasks[sock] = task
		outputs.append(sock)
		print(len(outputs))
		print(outputs)

while True:
	if len(tasks) == 0:
		break
	
	read, write, err = select.select(inputs, outputs, errors)
	print(f'R:{len(read)} W:{len(write)} E:{len(err)}')

	for sock in read:
		# data = listen_data(sock)
		data = 'oueah'
		tasks[sock].send(data)


	for sock in write:
		# 2
		msg, st = tasks[sock].next()
		if st == Status.CLOSE:
			assert st == Status.CLOSE
			print(f'[T] Message:\n{msg}')
			outputs.remove(sock)
			tasks[sock].close()


		if st == Status.GET:
			assert st == Status.GET
			# sock.sendall(msg)
			print(f'[T] Message:\n{msg}')
			outputs.remove(sock)
			inputs.append(sock)

		else:
			print(f'[ERROR] Status: {st}\nTask error in step 2')
			tasks[sock].close()
			outputs.remove(sock)


	for sock in err:
		outputs.remove(sock)
		tasks[sock].close()

