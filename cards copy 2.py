from math import comb
import itertools

hand_size = 6

input_deck = [
	['shino', 3],
	['saion', 2],
	['nazuki', 3],
	['baron', 3],
	['viscount', 2],
	['marquess', 2],
	['dominator', 1],
	['field', 4],
	['solo', 3],
	['small world', 3],
	['maxx', 3],
	['ash', 2],
	['golem', 3],
	# ['jizukiru', 1],
	['jizukiru', 2],
	['duelist', 1],
	['fossil', 1],
	# ['crossout', 1],
	['called', 2],
	# ['removal', 1],
	# ['wars', 1],
	# ['senet', 1],
]

# if a hand meets any rule, it is treated as valid

any_vaylantz = ['shino', 'baron', 'viscount', 'saion', 'nazuki', 'marquess', 'dominator']
high_vaylantz = ['nazuki', 'marquess', 'dominator']
low_vaylantz = ['baron', 'viscount', 'saion']
small_world_shino = ['ash', 'maxx', 'golem', 'jizukiru']

# basic rules are in the form of product of sums
# duplicates not supported, don't put the same cards in multiple groups

basic_rules = [
	[['shino']],
	[['solo'], any_vaylantz + ['field'] + ['wars']],
	[['small world'], small_world_shino],
]

def adversarial(hand):
	return False
	# count = 0
	# for unit in any_vaylantz:
	# 	count += hand.count(unit)
	# fieldable_count = count
	# if not ('field' in hand or 'wars' in hand) and not ('saion' in hand and 'nazuki' in hand) and not (('baron' in hand or 'viscount' in hand) and ('marquess' in hand or 'dominator' in hand)):
	# 	high_count = 0
	# 	for unit in high_vaylantz:
	# 		high_count += hand.count(unit)
	# 	fieldable_count -= high_count
	
	# return count >= 3 and fieldable_count >= 2


advanced_rules = [
	adversarial,
]

# end of user input

deck = []
for group in input_deck:
	for i in range(0, group[1]):
		deck.append(group[0])

valid_count = 0

for hand in itertools.combinations(deck, hand_size):
	# for a hand to be valid, only one rule needs to validate
	hand_valid = False
	for rule in basic_rules:
		# for a rule to be valid, every group in that rule needs to validate
		rule_valid = True
		for group in rule:
			# for a group to be valid, only one card in that group needs to validate
			group_valid = False
			for card in group:
				if card in hand:
					group_valid = True
					break
			if not group_valid:
				rule_valid = False
				break
		if rule_valid:
			hand_valid = True
			break
	
	if not hand_valid:
		for rule in advanced_rules:
			if rule(hand):
				hand_valid = True
				break
	
	if hand_valid:
		valid_count = valid_count + 1

print(f'deck size: {len(deck)} | hand size: {len(hand)}')
print(f'unique cards: {len(input_deck)} | validity rules: {len(basic_rules) + len(advanced_rules)}')
print(f'chance of valid hand: {valid_count / comb(len(deck), len(hand))}')

# TODO https://stackoverflow.com/questions/40351219/efficiently-check-if-an-element-occurs-at-least-n-times-in-a-list