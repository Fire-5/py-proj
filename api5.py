import select
import gen5_1
import time


def listen_data(sock):
    """Метод приема данных и формирование их в массив.
    На вход получает активный сокет. На выход выдает строку
    бинарных данных."""
    
    data = b''
    while True:
        raw = sock.recv(128)
        try:
            data += raw
            if len(raw) == 0:
                break

        except UnicodeDecodeError as e:
            print(f'[!] Unicode Error!\n{e}')
            continue

    if len(data) == 0:
        return b'NOT IMAGE'
    else:
        return data


def main():
    inputs = []
    outputs = []
    errors = []

    Status = gen5_1.Status

    # http://www.google.com/textinputassistant/tia.png
    urls1 = ['http://www.google.com']
    urls2 = [
        'http://www.google.com',
        'http://www.yandex.ru',
        'http://www.python.org',
        'http://www.py4inf.com',
        'https://vk.com',
        'https://www.rupython.com',
        'https://pythonworld.ru',
        'https://mail.ru/',
    ]

    # generators = map(gen5_1.generator, urls1)  # Вариант 1
    generators = map(gen5_1.generator, urls2)  # Вариант 2

    outputs, tasks = gen5_1.setup_generator(generators)

    while True:
        
        if len(outputs) + len(inputs) == 0:
            break

        read, write, err = select.select(inputs, outputs, errors, 3)
        print(f'[+] R:{len(read)} W:{len(write)} E:{len(err)}')
        for sock in write:
            st = None
            # 2
            msg, st = tasks[sock].send(None)
            print(f'[T] in WRITE {st}')
            # print(f'[TEST] Message:\n{msg}')

            if st == Status.GET:
                assert st == Status.GET
                sock.sendall(msg)
                inputs.append(sock)
                outputs.remove(sock)
                break

            if st == Status.ERROR:
                print(f'[E] Close socket in WRITE.')
                assert st == Status.CLOSE
                outputs.remove(sock)
                errors.append(sock)
                break

            # 4
            if st == Status.APPEND:
                for item in msg[0]:
                    outputs.append(item)
                tasks.update(msg[1])
                outputs.remove(sock)
                tasks[sock].close()


                break


            if st == Status.WAIT:
                break

            # 5
            if st == Status.CLOSE:
                assert st == Status.CLOSE
                outputs.remove(sock)
                tasks[sock].close()
                break

            # else:
            #     print(f'[ERROR] Status: {st}\nTask error in step 2')
            #     tasks[sock].close()
            #     outputs.remove(sock)

        for sock in read:
        	# 3
            time.sleep(0.03)
            data = listen_data(sock)
            staff, st = tasks[sock].send(None)
            print(f'[T] in READ {st}')
            # print(f'[TEST] input data:\n{data[:30]}\n...')

            if st != Status.READY:
                inputs.remove(sock)
                outputs.append(sock)
                break

            else:
                assert st == Status.READY, '[GEN] Bad yield'
                tasks[sock].send(data)
                inputs.remove(sock)
                outputs.append(sock)
                break

            

        for sock in err:
            print(f'[E] in ERROR')
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
