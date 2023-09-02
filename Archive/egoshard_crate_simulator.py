import random
import numpy

total = 0
count = 0
counts = []
for i in range(0, 10000000):
	count += 1
	total += random.randint(1, 3)
	if total >= 300:
		counts.append(count)
		total = 0
		count = 0

print(f'mean (should be 150): {sum(counts) / len(counts)}')
print(f'spark samples: {len(counts)}')

for i in range(135, 166):
	fails = 0
	for j in counts:
		if j > i:
			fails += 1
	print(f'chance of failed spark for {i}: {fails / len(counts)}')
