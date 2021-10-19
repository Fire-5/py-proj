a = 2 + 2
b = 4 - 2
c = 2 * 3
d = 9 / 2
print(a, b, c, d)

a1 = 33 // 5
b1 = 33 % 5
print(a1, b1)

a2 = 2 * 2 * 2
b2 = 2 ** 3

c2 = 1024 / 2 / 2 / 2
d2 = 1024 ** (1 / 10)
print(a2, b2, c2, d2)

F = 1
f = bool(F)
print(f)

########################################################

if a > 5:
	print('ver 1')

elif a == 5:
	print('ver 1.5')

else:
	print('ver 2')

 #  >  <
 # >= <=
 # == !=

if F:
	print('new ver 1\n\n\n\n\n\n')

##########################################################

arr = [1, 4, 2, 6, 2, 10]

for i in arr:
	print(i + 1)

print()

len(arr)

for i in range(55, 15, -4):
	print(i)

print()

for index, element in enumerate(arr):
	print(index, '-', element)
	if element > 5:
		arr[index] = 0

print(arr)

##########################################################

test_string = 'qwertyu' + "1234567" + """123
123123
123123
123123
"""

print(test_string)

string = '1234567890qwertyuiop[]'
s0 = string[2:9:2]
s1 = string[5:]
s2 = string[:7]
s3 = string[3]
s4 = string[::2]

print(s1, s2, s3, s4)