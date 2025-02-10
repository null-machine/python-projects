import numpy as np
import itertools
import sys

# 55 ^ 4 * 34 = 311 121 250

# store hands as np arrays that are 34 long
# 1p~9p, 1s~9s, 1m~9m, 1z~7z



melds = []

for i in range(0, 34):
	meld = [0] * 34
	meld[i] = 3
	melds.append(np.array(meld, dtype=np.int8))

for i in range(0, 7):
	meld = [0] * 34
	meld[i] = 1
	meld[i + 1] = 1
	meld[i + 2] = 1
	melds.append(np.array(meld, dtype=np.int8))

for i in range(9, 16):
	meld = [0] * 34
	meld[i] = 1
	meld[i + 1] = 1
	meld[i + 2] = 1
	melds.append(np.array(meld, dtype=np.int8))

for i in range(18, 25):
	meld = [0] * 34
	meld[i] = 1
	meld[i + 1] = 1
	meld[i + 2] = 1
	melds.append(np.array(meld, dtype=np.int8))

hands = []

for melds in itertools.combinations_with_replacement(melds, 4):
	for i in range(0, 34):
		hand = melds[0] + melds[1] + melds[2] + melds[3]
		hand[i] += 2
		if np.max(hand) < 5:
			hands.append(hand)

data = np.array(hands, dtype=np.int8)
np.save('hands.npy', data)

np.set_printoptions(threshold=sys.maxsize)
print(data[0])
# print(data)


# data = np.load('test.npy')
# print(data)