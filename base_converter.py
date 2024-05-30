import string


def int_to_base(n):
	unit_base = 11
	digits = ['0', '1', '2', '&', '3', '4', '5', '6', '7', '8', '9']
	result = ''
	if n < 0:
		sign = '-'
		n = -n
	else:
		sign = ''
	while n > 0:
		q, r = divmod(n, unit_base)
		result += digits[r]
		n = q
	if result == '':
		result = '0'
	return sign + ''.join(reversed(result))

input = None

try:
	input = eval("1aoeuaeo + 19")
except:
	input = None

print(int_to_base(12))