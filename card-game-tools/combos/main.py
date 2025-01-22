import data
from lines import State, Step, Engine

if __name__ != '__main__':
	exit()

playbook: list[Step] = []

for card in data.all_vaylantz:
	for i in [5, 9]:
		playbook.append(Step(
			name = f'{card}_scale_{i}',
			group = None,
			# check = lambda state: f'{card}' in state.hand and state.field[i] == None,
			# check = lambda state: card in state.hand and state.field[i] == None,
			check = lambda state: print(f'{card} {state.hand} {card in state.hand} {state.field[i] == None} {card in state.hand and state.field[i] == None}@@'),
			delta = [
				lambda state: state.place_card_from_hand(card, i),
			]
		))
		# if card in data.low_vaylantz:
		# 	playbook.append(Step(
		# 		name = f'{card}_self_summon_{i - 5}',
		# 		group = f'{card}_self_summon',
		# 		check = lambda state: state.field[i] == card and state.field[i - 5] == None,
		# 		delta = [
		# 			lambda state: state.swap_cards(i, i - 5),
		# 			lambda state: state.set_vaylantz_lock(True),
		# 		]
		# 	))

state: State = State()
state.hand.append('priestess')

engine: Engine = Engine(state, playbook)
engine.compute_to_console()

