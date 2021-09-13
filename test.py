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

s = requests.Session()

s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get('https://httpbin.org/cookies')
print(r.text)

response = requests.get('http://python.org')
print("Status:", response.status_code)
print("Content-type:", response.headers['content-type'])
response.encoding
print(response.text[:500])

print()
r = response.request.headers
print("request", r)

