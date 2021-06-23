# -*- coding: utf-8 -*-
import socket

urls = []
file_urls = open('urls.txt')

for line in file_urls:
    print(line)
    line = line.replace('\n', '')
    nline = line.replace('https://', '')
    nline = nline.replace('http://', '')
    nline = nline.replace('www.', '')[:-1]
    print(nline)
    ip = socket.gethostbyname_ex(nline)
    urls.append(ip)
print(urls)







