import socket
import select

general_socket = socket.socket() # Создание сокета для подключения
general_socket.bind(('', 9090))  # Настройка (Интерфейс, Порт)
general_socket.listen(1)         # Режим прослушки (кол-во подключеений)

connect_socket, addres = general_socket.accept() # принятие подключения.
# Метод возвращает новый сокет для подключения и адрес клиента

# Выводим на экран того, кто подключился
print('connected:', addres)

# Бесконечный цикл для получения всех данных (любых размеров...)
while True:
    # Получаем информацию по 1024 байта
    data = connect_socket.recv(1024)
    print(" --->", data)
    if not data:
        break # Если данных нет, то выходим из цикла

    # ЗДЕСЬ ДОЛЖНА БЫТЬ РАБОТА С ПОЛУЧЕННЫМИ ДАННЫМИ
    # Мы возвращаем измененные данные назад
    connect_socket.send(data.upper())

connect_socket.shutdown()
connect_socket.close()            # Закрываем сокет
print("connect socket:", connect_socket)
#connect socket: <
#           socket.socket [closed]
#           fd=-1,
#           family=AddressFamily.AF_INET,
#           type=SocketKind.SOCK_STREAM, proto=0
#           >