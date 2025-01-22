from collections import deque
import typing
from typing import Callable
import copy

class Data:
	
	monster_zones: set[int] = [0, 1, 2, 3, 4, 10, 11]
	
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
	
	def update_field(self, index: int, card: str):
		# bypass issue related to subscript assignment
		self.field[index] = card
	
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
		return f'Field: {self.field} | Hand: {self.hand} | Dead Groups: {self.dead_groups}'

class Step:
	
	def __init__(
		self,
		*,
		name: str,
		group: str | None = None,
		check: Callable[[State], bool],
		# delta: list[Callable[[State], None]],
		delta: Callable[[State], None],
	):
		self.name = name
		self.group = group
		self.check = check
		self.delta = delta

class Engine:
	
	def __init__(self, state: State, playbook: list[Step]):
		self.state = state
		self.playbook = playbook
		
		# self.state_stack: list[State] = []
		# self.step_stack: list[Step] = []
		# self.state_links: dict[State, set[State]] = {}
		# self.step_log: dict[tuple[State, State], Step] = {}
		
		# self.explored_states = 
		self.state_queue: deque[State] = deque([state])
		self.combos: dict[State, list[list[str]]] = {state: [[]]}
	
	def compute_combos(self):
		print('[I] Computing combos...')
		while self.state_queue:
			state = self.state_queue.popleft()
			for step in self.playbook:
				if step.group not in state.dead_groups and step.check(state):
					# print(f'starting {step.name}')
					next_state = copy.deepcopy(state)
					if step.group is not None:
						next_state.dead_groups.add(step.group)
					step.delta(next_state)
					paths: list[list[str]] = copy.deepcopy(self.combos[state])
					for path in paths:
						path.append(step.name)
					if next_state in self.combos:
						for path in paths:
							self.combos[next_state].append(path)
					else:
						self.combos[next_state] = paths
					self.state_queue.append(next_state)
					# print(f'completed {step.name}')
	
	def write_combos(self, filename='lines.txt'):
		print('[I] Writing combos...')
		with open(f'lines.txt', 'w') as file:
			for state in self.combos:
				file.write(f'{state.to_string()}\n')
				for line in self.combos[state]:
					file.write(f'\t{line}\n')
				file.write(f'\n')
			
		
	
	

if __name__ != '__main__':
	exit()

playbook: list[Step] = []

# weird code ahead to bypass late binding
for card in Data.all_vaylantz:
	for i in [0, 4]:
		
		def check(i: int, card: str):
			def check(state: State):
				# print(f'scale check {card} {i} {card in state.hand} {state.field[i] == None}')
				return card in state.hand and state.field[i] == None
			return check
		def delta(i: int, card: str):
			def delta(state: State):
				state.place_card_from_hand(card, i)
			return delta
		playbook.append(Step(
			name = f'{card}_scale_{i}',
			group = None,
			check = check(i, card),
			delta = delta(i, card),
			# check = lambda state, _card=card: _card in state.hand and state.field[i] == None,
			# delta = [
			# 	lambda state, _card=card: state.place_card_from_hand(_card, i),
			# ]
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
				group = f'{card}_self_summon',
				check = check(i, card),
				delta = delta(i, card),
			))
		# elif card in Data.high_vaylantz:
			
		# priestess_search_ninja

state: State = State()
state.hand = ['priestess', 'baron', 'archer', 'viscount', 'marquis']

engine: Engine = Engine(state, playbook)
engine.compute_combos()
engine.write_combos()
