from math import comb

deck = 40
hand = 6
a = 6
b = 5
print(f'deck size: {deck} | hand size: {hand} | group sizes: {a}, {b}')

total = comb(deck, hand)
notA = comb(deck - a, hand)
notB = comb(deck - b, hand)
nor = comb(deck - a - b, hand)
nand = notA + notB - nor

print(f'chance of one from each group: {1 - nand / total}')
print(f'chance of one from either group: {1 - nor / total}')