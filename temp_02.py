# -*- coding: utf-8 -*-
from subprocess import Popen, CREATE_NEW_CONSOLE
import os

process_list = [] #сюда будут попадать все клиентские процессы
while True:
    user = input('Запустить 10 клиентов (start) / Закрыть клиентов (close) / Выйти (quit) ')
    if user == "quit":
        break
    elif user == "start":
        for i in range(10):
            process_list.append(Popen("python temp_04.py", creationflags =
                                      CREATE_NEW_CONSOLE))
            print("Запущено 10 клиентов")
    elif user == "close":
        for process in process_list:
            process.kill()
            process_list.clear() #очищаем список