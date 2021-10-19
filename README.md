# py-proj
 svzcom | mobilfon test

Тестовое задание на замещение вакантной должности «Программиста-разработчика» по специализации «Python разработчик»

Версия: 1.0

Требуется разработать сетевое приложение и реализовать асинхронный режим работы с логикой задаваемой генератором.

Детальные требования:
1.  Логика сетевого клиента: 3 или более последовательных HTTP запроса с анализом полученных данных.
2.  Логика сетевого клиента должна быть реализована в виде генератора.
3.  Одновременное выполнение нескольких логических цепочек (генераторов)
4.  По окончанию выполнения всех логических цепочек, вывести результат работы в STDOUT и завершить работу приложения.
5.  Максимальное количество потоков для приложения: 1
6.  Основной поток должен блокироваться только для ожидания сетевых событий или таймеров.
7.  Реализация сетевого уровня: на уровне сокетов.
8.  Реализация HTTP протокола: на усмотрение исполнителя.
9.  HTTP ресурс для запроса и анализ полученных данных: на усмотрение исполнителя (Любой подходящий ресурс в интернете).
10. Реализация диспетчера обработки асинхронных событий: на основе select или иного аналогичного механизма для асинхронной работы с сокетами.
11. Формат входных данных, таких как HTTP ресурс, количество одновременных логических цепочек и иная информация: на усмотрение исполнителя.
12. Требование к версии python: не выше 3.6.
13. Результат работы представить в виде архива с python приложением и краткой инструкцией.
14. Результат работы предоставить на электронную почту и позвонить по телефону, сообщить, что отправили.

Список файлов с пояснениями:
 - api5.py
 Основной файл, который работает с циклом select, отправляет и принимает данные и управляет всеми основными действиями приложения.
 - gen5_1.py
 Генератор, который формирует запрос к сайту, парсит данные и решает что с ними делать. Так же набор необходимых функций.