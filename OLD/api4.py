import select
from gen4 import Status
from gen4 import Generator_url as gen

inputs = []
outputs = []
errors = []

tasks = [gen('http://www.google.com')]

while True:
	read, write, err = select.select(inputs, outputs, errors)

	for sock in read:
		# msg = listen(sock)
		msg = 'stroka'
		tasks[sock].next(msg)
		msg, st = tasks[sock].next()
		assert st == Status.DONE, 'Статус должен быть DONE'
		print(f'[+] {st} in read')

	for sock in write:
		msg, st = tasks[sock].next()

		if st == Status.GET:
			print(f'[+] {st} in write')
			# sock.sendall(msg)
			outputs.remove(sock)
			inputs.remove(sock)

	for sock in errors:
		print(f'[-] Task close')
		tasks[sock].close()
		inputs.remove(sock)
		outputs.remove(sock)
		errors.remove(sock)

	if len(inputs + outputs + errors) == 0:
		break
