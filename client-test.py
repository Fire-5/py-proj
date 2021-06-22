# -*- coding: utf-8 -*-
import socket

finput = open('input.txt', 'r')
foutput = open('output.txt', 'w')

connect_socket = socket.socket() # Создание сокета для подключения
# Подключение по указанному адресу (IP, PORT)
connect_socket.connect(('localhost', 9090))

# Отправка строки, закодированной в байты.
for line in finput:
    out_data = line
    connect_socket.send(str.encode(out_data))

while True:
    # Получаем информацию по 1024 байта
    in_data = connect_socket.recv(1024)
    str_data = in_data.decode()
    foutput.write(str_data)
    print(" --->", str_data)
    if not in_data:
        break # Если данных нет, то выходим из цикла

connect_socket.shutdown()
connect_socket.close()           # Закрываем сокет
foutput.close()
finput.close()

