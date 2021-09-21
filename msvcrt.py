import os
import msvcrt
import time

ST_TIME = time.time()
message = []
while True:
    line = ''
    while time.time() - ST_TIME < 5:

        if msvcrt.kbhit():
            c = msvcrt.getch().decode('utf-8')

            if ord(c) == 13:
                break
            line = line + c
            print(c, end = '')

    ST_TIME = time.time()
    if line == 'quit':
        break
    print()
    message.append(line + '\n')

print(message)