# Write a python function that will print all the numbers below 100.
# The program will also write "THREE" if the number is a multiple of 3,
# "FIVE" if it is a multiple of 5 or "BOTH" if the number is a multiple of both.

for i in range(100):
	print(i)
	x = i % 3 == 0
	y = i % 5 == 0
	if x and y:
		print('BOTH')
	elif x:
			print('THREE')
	elif y:
			print('FIVE')
