from collections import deque
import typing
from typing import Callable
import copy
import json

class Data:
	
	monsters: set[str] = {'sbt', 'cannahawk', 'rampengu', 'apelio', 'pettlephin', 'elder', 'wen', 'winda'}
	tamers: set[str] = {'sbt', 'elder', 'wen', 'winda'}
	beasts: set[str] = {'sbt', 'cannahawk', 'rampengu', 'apelio', 'pettlephin'}
	

class Stage:
	
	def __init__(
		self,
		*,
		hand: dict[str, int] = {},
		field: dict[str, int] = {},
		grave: dict[str, int] = {},
		exile: dict[str, int] = {},
		tags: set[str] = set(),
		normal_summons: int = 1,
	) -> bool:
		self.hand = hand
		self.field = field
		self.grave = grave
		self.exile = exile
		self.tags = tags
		self.normal_summons = normal_summons
	
	def __eq__(self, other):
		return (self.hand == other.hand and
			self.field == other.field and
			self.grave == other.grave and
			self.exile == other.exile and
			self.normal_summons == other.normal_summons)
	
	def __hash__(self):
		data = {
			'hand': self.hand,
			'field': self.field,
			'grave': self.grave,
			'exile': self.exile,
			'tags': sorted(self.tags),
			'normal_summons': self.normal_summons,
		}
		return hash(json.dumps(data, sort_keys=True))
	
	def has(self, target: str, card: str) -> bool:
		target = getattr(self, target)
		return card in target and target[card] > 0
	
	def add(self, target: str, card: str) -> None:
		target = getattr(self, target)
		target[card] = target.get(card, 0) + 1
	
	def remove(self, target: str, card: str) -> None:
		target = getattr(self, target)
		target[card] = target[card] - 1
		if target[card] <= 0:
			target.pop(card)
	
	def move(self, source: str, output: str, card: str) -> None:
		self.remove(source, card)
		self.add(output, card)
	
	def to_string(self):
		data = []
		if self.field:
			data.append(f'Field: {self.field}')
		if self.hand:
			data.append(f'Hand: {self.hand}')
		if self.grave:
			data.append(f'Grave: {self.grave}')
		if self.exile:
			data.append(f'Exile: {self.exile}')
		# if self.tags:
		# 	data.append(f'{self.tags}')
		return ' | '.join(data)

class Step:
	
	def __init__(
		self,
		*,
		name: str,
		tags: set[str] | None = None,
		check: Callable[[Stage], bool],
		delta: Callable[[Stage], None],
	) -> None:
		self.name = name
		self.tags = tags
		self.check = check
		self.delta = delta

# class Playbook: # implement to make scan step O(n) instead of theta(n)
	
# 	def __init__(
# 		self,
# 		*,
# 		name: str,
#		global_steps: list[Step],
# 		hand_steps: list[Step],
# 		field_steps: list[Step],
# 		grave_steps: list[Step],
# 		exile_steps: list[Step],
# 	) -> None:
# 		self.name = name
# 		self.hand_steps = hand_steps
# 		self.field_steps = field_steps
# 		self.grave_steps = grave_steps
# 		self.exile_steps = exile_steps

class Engine:
	
	def __init__(self, stage: Stage, library: list[Step]):
		self.stage = stage
		self.library = library
		
		self.stage_queue: deque[Stage] = deque([stage])
		self.lines: dict[Stage, list[list[str]]] = {stage: [[]]}
	
	def compute_combos(self):
		print(f'[I] Computing lines with {len(self.library)} rules')
		while self.stage_queue:
			stage = self.stage_queue.popleft()
			for step in self.library:
				tags_valid = not step.tags or not bool(step.tags & stage.tags)
				if tags_valid and step.check(stage):
					next_state = copy.deepcopy(stage)
					if step.tags is not None:
						next_state.tags = next_state.tags | step.tags
					step.delta(next_state)
					paths: list[list[str]] = copy.deepcopy(self.lines[stage])
					for path in paths:
						path.append(step.name)
					if next_state in self.lines:
						for path in paths:
							self.lines[next_state].append(path)
					else:
						self.lines[next_state] = paths
						self.stage_queue.append(next_state)
	
	def write_combos(self, filename='lines.txt'):
		print(f'[I] Writing lines for {len(self.lines)} endboards')
		with open(f'lines.txt', 'w') as file:
			for stage in self.lines:
				file.write(f'{stage.to_string()}\n')
				for line in self.lines[stage]:
					file.write(f'\t{line}\n')
				file.write(f'\n')

if __name__ != '__main__':
	exit()

library: list[Step] = []

for card in Data.monsters:
	# normal summons
	def check(card: str) -> Callable[[Stage], bool]:
		def check(stage: Stage) -> bool:
			return stage.has('hand', card) and stage.normal_summons > 0
		return check
	def delta(card: str) -> Callable[[Stage], None]:
		def delta(stage: Stage) -> None:
			stage.move('hand', 'field', card)
			if card != 'elder':
				stage.normal_summons -= 1
		return delta
	library.append(Step(
		name = f'{card}_normal',
		tags = None,
		check = check(card),
		delta = delta(card),
	))
	# cannahawk sopt
	if card != 'cannahawk':
		def delta(card: str) -> Callable[[Stage], None]:
			def delta(stage: Stage) -> None:
				stage.add('exile', card)
			return delta
		library.append(Step(
			name = f'cannahawk_sopt_{card}',
			tags = {f'{card}_deck', 'cannahawk_sopt'},
			check = lambda stage: stage.has('field', 'cannahawk'),
			delta = delta(card),
		))

for tamer in Data.tamers:
	for beast in Data.beasts:
		if tamer == beast:
			continue # sbt
		# ultihawk contact
		def check(tamer: str, beast: str) -> Callable[[Stage], bool]:
			def check(stage: Stage) -> bool:
				return stage.has('field', tamer) and stage.has('field', beast)
			return check
		def delta(tamer: str, beast: str) -> Callable[[Stage], None]:
			def delta(stage: Stage) -> None:
				stage.move('field', 'exile', tamer)
				stage.move('field', 'exile', beast)
				stage.add('field', 'ultihawk')
				stage.tags -= {f'{tamer}_sopt', f'{beast}_sopt'}
			return delta
		library.append(Step(
			name = f'ultihawk_contact_{tamer}_{beast}',
			tags = {'ultihawk_deck'},
			check = check(tamer, beast),
			delta = delta(tamer, beast),
		))
		# ultihawk bounce
		def check(tamer: str, beast: str) -> Callable[[Stage], bool]:
			def check(stage: Stage) -> bool:
				return stage.has('field', 'ultihawk') and stage.has('exile', tamer) and stage.has('exile', beast)
			return check
		def delta(tamer: str, beast: str) -> Callable[[Stage], None]:
			def delta(stage: Stage) -> None:
				stage.remove('field', 'ultihawk')
				stage.move('exile', 'field', tamer)
				stage.move('exile', 'field', beast)
				stage.tags -= {'ultihawk_deck'}
			return delta
		library.append(Step(
			name = f'ultihawk_bounce_{tamer}_{beast}',
			tags = {f'{tamer}_special', f'{beast}_special'},
			check = check(tamer, beast),
			delta = delta(tamer, beast),
		))

stage: Stage = Stage()
stage.hand = {'cannahawk': 1, 'elder': 1}
stage.tags = {'cannahawk_deck', 'elder_deck'}
# stage.normal_summons = 2

engine: Engine = Engine(stage, library)
engine.compute_combos()
engine.write_combos()
