# -*- coding: utf-8 -*-
from socket import *
import sys

def client():
    with socket(AF_INET, SOCK_STREAM) as sock:
        address = ('localhost', 8888)
        sock.connect(address)

        while True:
            message = input(' >>> ')
            sock.send(message.encode('utf-8'))
            recive = sock.recv(1024).decode('utf-8')
            print(' <<< ', recive)

if __name__ == '__main__':
    client()