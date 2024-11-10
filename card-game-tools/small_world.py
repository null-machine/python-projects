cards = []
card_names = []

with open('small_world.txt', encoding='utf-8') as file:
	for line in file:
		if line.strip() == '---':
			break
		card = line.strip().split(' ')
		cards.append(card)
		card_names.append(card[0])

cards.sort()
card_names.sort()

while True:
	query = input('Input card name: ')
	target = ''
	for card in cards:
		if card[0] == query:
			target = card
	if target == '':
		print('Card not found, consult `small_world.txt` for valid cards')
		print('---')
		continue
	chains = []
	starters = []
	for bridge in cards:
		match_count = 0
		for i in range(0, len(target)):
			if bridge[i] == target[i]:
				match_count += 1
		if match_count == 1:
			for starter in cards:
				match_count = 0
				for i in range(0, len(target)):
					if bridge[i] == starter[i]:
						match_count += 1
				if match_count == 1 and starter != target:
					# success_count += 1
					chains.append([target[0], bridge[0], starter[0]])
					starters.append(starter[0])
					# print()
	chains.sort(key=lambda x: x[2])
	starters = set(starters)
	for chain in chains:
		print(f'{chain[0]} | {chain[1]} | {chain[2]}')
	for name in card_names:
		if name not in starters and name != target[0]:
			print(f'no chain: {name}')
	print(f'--- {len(starters)} / {len(cards) - 1} ---')