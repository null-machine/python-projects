from collections import deque
import typing
from typing import Callable
import copy

class Data:
	
	monster_zones: set[int] = [5, 6, 7, 8, 9, 10, 11]
	main_monster_zones: set[int] = [5, 6, 7, 8, 9]
	
	all_vaylantz: set[str] = {'priestess', 'baron', 'viscount', 'archer', 'ninja', 'marquis', 'duke', 'warrior'}
	low_vaylantz: set[str] = {'priestess', 'baron', 'viscount', 'archer'}
	high_vaylantz: set[str] = {'ninja', 'marquis', 'duke', 'warrior'}
	fire_vaylantz: set[str] = {'baron', 'viscount', 'marquis', 'duke'}
	water_vaylantz: set[str] = {'priestess', 'archer', 'ninja', 'warrior'}
	

class State:
	
	# field
	#	12	10		11	13
	#	5	6	7	8	9
	#	0	1	2	3	4
	
	def __init__(
		self,
		*,
		field: list[str | None] = [None] * 14,
		hand: list[str] = [],
		grave_extra: list[str] = [],
		dead_groups: set[str] = set(),
	):
		self.field = field
		self.hand = hand
		self.grave_extra = grave_extra
		self.dead_groups = dead_groups
		
		self.vaylantz_lock = False
		self.effect_lock = False
	
	def place_card_from_hand(self, card: str, index: int):
		# print(f'place card from hand {card} {self.hand}')
		self.hand.remove(card)
		self.field[index] = card
	
	def swap_cards(self, index_a: int, index_b: int):
		buffer = self.field[index_a]
		self.field[index_a] = self.field[index_b]
		self.field[index_b] = buffer
	
	# def check_isomer(self, state: State):
	# 	pass
	
	def to_string(self):
		return f'Field: {self.field} | Hand: {self.hand} | Dead Groups: {self.dead_groups}@{self.grave_extra}{self.vaylantz_lock}{self.effect_lock}'


class Step:
	
	def __init__(
		self,
		*,
		name: str,
		groups: str | None = None,
		check: Callable[[State], bool],
		# delta: list[Callable[[State], None]],
		delta: Callable[[State], None],
	):
		self.name = name
		self.groups = groups
		self.check = check
		self.delta = delta

class Engine:
	
	def __init__(self, state: State, playbook: list[Step]):
		self.state = state
		self.playbook = playbook
		
		self.state_queue: deque[State] = deque([state])
		self.combos: dict[str, list[list[str]]] = {state.to_string(): [[]]}
	
	def compute_combos(self):
		print('[I] Computing combos...')
		while self.state_queue:
			state = self.state_queue.popleft()
			for step in self.playbook:
				groups_valid = True
				if step.groups:
					for group in step.groups:
						if group in state.dead_groups:
							groups_valid = False
							break
				if groups_valid and step.check(state):
					# print(f'starting {step.name}')
					next_state = copy.deepcopy(state)
					if step.groups is not None:
						for group in step.groups:
							next_state.dead_groups.add(group)
					step.delta(next_state)
					paths: list[list[str]] = copy.deepcopy(self.combos[state.to_string()])
					for path in paths:
						path.append(step.name)
					if next_state.to_string() in self.combos:
						for path in paths:
							self.combos[next_state.to_string()].append(path)
					else:
						self.combos[next_state.to_string()] = paths
						self.state_queue.append(next_state)
	
	def write_combos(self, filename='lines.txt'):
		print('[I] Writing combos...')
		with open(f'lines.txt', 'w') as file:
			for key in self.combos:
				file.write(f'{key.split('@')[0]}\n')
				for line in self.combos[key]:
					file.write(f'\t{line}\n')
				file.write(f'\n')
			
		
	
	

if __name__ != '__main__':
	exit()

playbook: list[Step] = []

def check(state: State):
	for i in Data.main_monster_zones:
		if state.field[i] == 'priestess':
			return True
	return False
def delta(state: State):
	state.hand.append('solo')
playbook.append(Step(
	name = f'priestess_search_solo',
	groups = [f'priestess_ignite'],
	check = check,
	delta = delta,
))

# weird code ahead to bypass late binding
for card in Data.all_vaylantz:
	
	# if card not 'priestess':
	# 	def check(card: str):
	# 		def check(state: State):
	# 			for i in Data.main_monster_zones:
	# 				if state[i] == 'priestess':
	# 					return True
	# 			return False
	# 		return check
	# 	def delta(card: str):
	# 		def delta(state: State):
	# 			state.hand.append(card)
	# 		return delta
	# 	playbook.append(Step(
	# 		name = f'priestess_search_{card}',
	# 		groups = [f'{card}_deck', 'priestess_shift']
	# 		check = check(card),
	# 		delta = delta(card),
	# 	))
	
	for i in [0, 4]:
		
		def check(i: int, card: str):
			def check(state: State):
				return card in state.hand and state.field[i] == None
			return check
		def delta(i: int, card: str):
			def delta(state: State):
				state.place_card_from_hand(card, i)
			return delta
		playbook.append(Step(
			name = f'{card}_scale_{i}',
			groups = None,
			check = check(i, card),
			delta = delta(i, card),
		))
		
		if card in Data.low_vaylantz:
			def check(i: int, card: str):
				def check(state: State):
					return state.field[i] == card and state.field[i + 5] == None
				return check
			def delta(i: int, card: str):
				def delta(state: State):
					state.swap_cards(i, i + 5)
					state.vaylantz_lock = True
				return delta
			playbook.append(Step(
				name = f'{card}_self_summon_{i + 5}',
				groups = [f'{card}_self_summon'],
				check = check(i, card),
				delta = delta(i, card),
			))
		# elif card in Data.high_vaylantz:
		
		if card == 'priestess':
			def check(i: int, card: str):
				def check(state: State):
					return 'solo' in state.hand and state.field[i] == None
				return check
			def delta(i: int, card: str):
				def delta(state: State):
					state.field[i] = card
				return delta
			playbook.append(Step(
				name = f'solo_scale_{card}_{i}',
				groups = ['solo_cast'],
				check = check(i, card),
				delta = delta(i, card),
			))
		else:
			def check(i: int, card: str):
				def check(state: State):
					return 'solo' in state.hand and state.field[i] == None
				return check
			def delta(i: int, card: str):
				def delta(state: State):
					state.field[i] = card
				return delta
			playbook.append(Step(
				name = f'solo_scale_{card}_{i}',
				groups = ['solo_cast', f'{card}_deck'],
				check = check(i, card),
				delta = delta(i, card),
			))

# 	def check(card: str):
	# 		def check(state: State):
	# 			for i in Data.main_monster_zones:
	# 				if state[i] == 'priestess':
	# 					return True
	# 			return False
	# 		return check
	# 	def delta(card: str):
	# 		def delta(state: State):
	# 			state.hand.append(card)
	# 		return delta
	# 	playbook.append(Step(
	# 		name = f'{card}_scale_{i}',
	# 		groups = [f'{card}_deck', 'priestess_shift']
	# 		check = check(card),
	# 		delta = delta(card),
	# 	))

state: State = State()
# state.hand = ['priestess', 'baron', 'archer', 'viscount', 'marquis']
state.hand = ['priestess']

engine: Engine = Engine(state, playbook)
engine.compute_combos()
engine.write_combos()
