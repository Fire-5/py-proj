# -*- coding: utf-8 -*-
import socket

host = '178.248.234.66'
port = 443
addr = (host,port)

Request = {'Sline':'GET / HTTP/1.1',
           'Headers':'Host: catalog/noutbuki/ \nAccept: text/html',
           'MBody':''
}

connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_socket.connect(addr)
req = Request['Sline']+"\n"+Request['Headers']
connect_socket.send(req.encode())
print(">>> ", req, '\n')

while True:
    # Получаем информацию по 1024 байта
    in_data = connect_socket.recv(1024)
    str_data = in_data.decode()
    print("<<< ", str_data)
    if not in_data:
        break # Если данных нет, то выходим из цикла


connect_socket.close()

# name_gen = (st for st in in_data if "Ноутбук" in st)
# for item in name_gen:
#     print(item)