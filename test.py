import aiohttp, asyncio, requests

# async def main():

#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://python.org') as response:

#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])

#             html = await response.text()
#             html.split('\n')
#             print("Body:", html[:50])

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


# s = requests.Session()

# s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
# r = s.get('https://httpbin.org/cookies')
# print(r.text)

# response = requests.get('http://python.org')
# print("Status:", response.status_code)
# print("Content-type:", response.headers['content-type'])
# response.encoding
# print(response.text[:500])

# print()
# r = response.request.headers



import requests
req = requests.Request('GET', 'https://pastebin.pl/')
r = req.prepare()

s = requests.Session()
resp = s.send(r)
'''
['__class__', 
'__delattr__', 
'__dict__', 
'__dir__', 
'__doc__', 
'__eq__', 
'__format__', 
'__ge__', 
'__getattribute__', 
'__gt__', 
'__hash__', 
'__init__', 
'__init_subclass__', 
'__le__', 
'__lt__', 
'__module__', 
'__ne__', 
'__new__', 
'__reduce__', 
'__reduce_ex__', 
'__repr__', 
'__setattr__', 
'__sizeof__', 
'__str__', 
'__subclasshook__', 
'__weakref__', 
'_body_position', 
'_cookies', 
'_encode_files', 
'_encode_params', 
'_get_idna_encoded_host', 
'body', 
'copy', 
'deregister_hook', 
'headers', 
'hooks', 
'method', 
'path_url', 
'prepare', 
'prepare_auth', 
'prepare_body', 
'prepare_content_length', 
'prepare_cookies', 
'prepare_headers', 
'prepare_hooks', 
'prepare_method', 
'prepare_url', 
'register_hook', 
'url']
'''
print("request\n", r.headers, '\n\n', resp.headers)
