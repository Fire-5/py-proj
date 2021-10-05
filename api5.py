import select
import gen5


def listen_data(sock):
    """ метод приема данных и формирование их в массив данных"""
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


def main():
    inputs = []
    outputs = []
    errors = []

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

    generators = map(gen5.generator, urls1)  # Вариант 1
    # generators = map(gen5.generator, urls2)  # Вариант 2

    outputs, tasks = gen5.setup_generator(generators)

    while True:

        read, write, err = select.select(inputs, outputs, errors, 3)
        print(f'[+] R:{len(read)} W:{len(write)} E:{len(err)}')

        for sock in write:
            # 2
            msg, st = tasks[sock].send(None)
            print(f'[TEST] in WRITE {st}')
            print(f'[TEST] Message:\n{msg}')

            if st == Status.GET:
                assert st == Status.GET
                sock.sendall(msg)
                inputs.append(sock)
                outputs.remove(sock)
                break

            if st == Status.CLOSE:
                print(f'[CLOSE] Close socket in WRITE.')
                assert st == Status.CLOSE
                outputs.remove(sock)
                tasks[sock].close()
                break

            if st == Status.ERROR:
                print(f'[ERROR] Close socket in WRITE.')
                assert st == Status.CLOSE
                outputs.remove(sock)
                errors.append(sock)
                break

            else:
                print(f'[ERROR] Status: {st}\nTask error in step 2')
                tasks[sock].close()
                outputs.remove(sock)

        for sock in read:
            data = listen_data(sock)
            staff, st = tasks[sock].send(None)
            print(f'[TEST] in READ {st}')
            print(f'[TEST] input data:\n{data[:16]}\n...')

            if st != Status.READY:
                inputs.remove(sock)
                outputs.append(sock)

            else:
                assert st == Status.READY, '[GEN] Bad yield'
                tasks[sock].send(data)
                inputs.remove(sock)
                outputs.append(sock)

            break

        for sock in err:
            print(f'[ERROR] in ERROR')
            if sock in inputs:
                inputs.remove(sock)
            if sock in outputs:
                outputs.remove(sock)
            if sock in errors:
                errors.remove(sock)
            tasks[sock].close()
            break


if __name__ == '__main__':
    main()
    print("[FINISH]")
