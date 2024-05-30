import random
import statistics

correct = 0
total = 0

for _ in range(0, 1000):
	raw = []

	for i in range(0, 100):
		raw.append(random.randint(0, 1))

	counts = []
	count = 0
	prev = None

	for i in raw:
		if prev == i:
			count += 1
		else:
			counts.append(count + 1)
			count = 0
		prev = i
	counts.append(count + 1)
	counts = counts[1:]

	group_size = statistics.mean(counts)

	# print(raw)
	# print(counts)
	# print(group_size)

	tail = raw[-2:]
	guess = None

	if tail[0] == tail[1]:
		if tail[0] == 0:
			guess = 1
		else:
			guess = 0
	else:
		if group_size < 2:
			guess = tail[1]
		else:
			if tail[1] == 0:
				guess = 1
			else:
				guess = 0

	answer = random.randint(0, 1)
	total += 1
	if guess == answer:
		correct += 1

	# print(guess, answer)
print(correct, total, correct / total)