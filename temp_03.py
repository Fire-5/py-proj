# -*- coding: utf-8 -*-

import aiohttp
import asyncio
# Новая библиотека, для парсинга xml
from lxml import etree


async def fetch(session, url):
    async with session.get(url) as response:
        # Возвращаем ответ в байтах
        return await response.content.read()


async def main():
    async with aiohttp.ClientSession() as session:
        xml_str = await fetch(session, 'https://www.google.com/sitemap.xml')
        print('xml_str = ',type(xml_str), ' : ', )
        root = etree.fromstring(xml_str)
        print('root = ',type(root),'\n\n\n')

        for url in root.xpath('//*[local-name()="loc"]/text()'):
            print(url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()