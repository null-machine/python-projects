import typing
from typing import Callable

class Data:
	
	all_vaylantz: set[str] = {'priestess', 'baron', 'viscount', 'archer', 'ninja', 'marquis', 'duke', 'warrior'}
	low_vaylantz: set[str] = {'priestess', 'baron', 'viscount', 'archer'}
	

class State:
	
	# field
	#	12	10		11	13
	#	0	1	2	3	4
	#	5	6	7	8	9
	
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
		self.hand.remove(card)
		self.field[index] = card
	
	def swap_cards(self, index_a: int, index_b: int):
		buffer = self.field[index_a]
		self.field[index_a] = self.field[index_b]
		self.field[index_b] = buffer
	

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
	
	def compute_to_console(self):
		print(f'computing to console {len(self.playbook)}')
		for step in self.playbook:
			print(step.name)
			if step.group not in self.state.dead_groups and step.check(self.state):
				self.state.dead_groups.add(step.group)
				step.delta(self.state)
				print(f'### {step.name} {state.dead_groups} {self.state.field}')
				# for function in step.delta:
				# 	function(self.state)
	
	# def compute_all_to_file(filename: str):

if __name__ != '__main__':
	exit()

playbook: list[Step] = []

# weird code ahead to bypass late binding
for card in Data.all_vaylantz:
	for i in [5, 9]:
		
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
			group = None,
			check = check(i, card),
			delta = delta(i, card),
			# check = lambda state, _card=card: _card in state.hand and state.field[i] == None,
			# delta = [
			# 	lambda state, _card=card: state.place_card_from_hand(_card, i),
			# ]
		))
		
		def check(i: int, card: str):
			def check(state: State):
				return state.field[i] == card and state.field[i - 5] == None
			return check
		def delta(i: int, card: str):
			def delta(state: State):
				state.swap_cards(i, i - 5)
				state.vaylantz_lock = True
			return delta
		if card in Data.low_vaylantz:
			playbook.append(Step(
				name = f'{card}_self_summon_{i - 5}',
				group = f'{card}_self_summon',
				check = check(i, card),
				delta = delta(i, card),
			))

state: State = State()
state.hand = ['priestess', 'baron', 'marquis']

engine: Engine = Engine(state, playbook)
engine.compute_to_console()

