import itertools
import gzip
import numpy as np
import sys

# store hands as np arrays that are 34 long
# 1p~9p, 1s~9s, 1m~9m, 1z~7z
np.set_printoptions(threshold=sys.maxsize)

def save(data, name):
	file = gzip.GzipFile(f'{name}.gz', 'w')
	np.save(file, data)
	file.close()

def load(name):
	file = gzip.GzipFile(f'{name}.gz', 'r')
	return np.load(file)

data = load('raw_hands')
print(data[343456], len(data))

valid_hands = []
for hand in data:
	if (
		hand[0] + hand[8] + hand[9] + hand[17] + hand[18] + hand[26] +
		hand[27] + hand[28] + hand[29] + hand[30] + hand[31] + hand[32] + hand[33] == 0
	):
		valid_hands.add(hand)
		continue
	