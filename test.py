import socket
import select

# http://www.google.com/images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png
# https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('www.py4inf.com', 80))
# s.sendall(b'GET /images/branding/googlelogo/1x/googlelogo_white_background_color_272x92dp.png HTTP/1.1\r\nHOST: www.google.com\r\n\r\n')
s.sendall(b"GET /cover.jpg HTTP/1.1\r\nHOST: www.py4inf.com\r\n\r\n")
reply = b''

while select.select([s], [], [], 3)[0]:
    data = s.recv(2048)
    if not data:
        break
    reply += data

reply = reply.split(b'\r\n\r\n')
print(reply[:30], '\n\n\n\n')
headers = reply[0]
print(headers)
image = reply[1]


# save image
f = open('image.png', 'wb')
f.write(image)
f.close()

# https://httpbin.org/image/png


