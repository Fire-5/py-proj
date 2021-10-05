import os
import requests

r = requests.Request('GET', 'https://httpbin.org/image/png')
req = r.prepare()
# body
# copy
# deregister_hook
# headers
# hooks
# method
# path_url
# prepare
# prepare_auth
# prepare_body
# prepare_content_length
# prepare_cookies
# prepare_headers
# prepare_hooks
# prepare_method
# prepare_url
# register_hook
# url
print(req.url.replace(req.path_url,''))


# raw_url = 'ttttt'
# img = ['', 'test']
# path = os.getcwd()
#
# if not os.path.exists(f"data//{raw_url}"):
#     os.mkdir(f"data//{raw_url}")
#
#
# f = open(f'data//{raw_url}//{img[1]}.txt', 'wb')
# f.write(b'1111111111111111111111112')
# f.close()
#
# print(path)