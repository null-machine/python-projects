def factorial(n):
	product = 1
	while n >= 1:
		product *= n
		n -= 1
	return product

def choose(n, r):
	return factorial(n) / (factorial(r) * factorial(n - r))


