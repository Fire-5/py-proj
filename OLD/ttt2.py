def gen(string):
	while True:
		a = string[:5]
		b = string[5:]
		string = yield a, b



def main():
	g = gen('1234567890')
	a, b = g.send(None)
	print(a, b)

	a, b = g.send('abcdifghijk')
	print(a, b)

if __name__ == '__main__':
	main()