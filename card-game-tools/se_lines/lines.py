from collections import deque
import typing
from typing import Callable
import copy
import json
from stage import Stage

class Data:
	
	monsters: set[str] = {'sbt', 'cannahawk', 'rampengu', 'apelio', 'pettlephin', 'elder', 'wen', 'winda'}
	tamers: set[str] = {'sbt', 'elder', 'wen', 'winda'}
	beasts: set[str] = {'sbt', 'cannahawk', 'rampengu', 'apelio', 'pettlephin'}


class Rule:
	
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

class Engine:
	
	def __init__(self, stage: Stage, playbook: list[Rule]):
		self.stage = stage
		self.playbook = playbook
		
		self.stage_queue: deque[Stage] = deque([stage])
		self.lines: dict[Stage, list[list[str]]] = {stage: [[]]}
	
	def compute_combos(self):
		print(f'[I] Computing lines with {len(self.playbook)} rules')
		while self.stage_queue:
			stage = self.stage_queue.popleft()
			for rule in self.playbook:
				tags_valid = not rule.tags or not bool(rule.tags & stage.tags)
				if tags_valid and rule.check(stage):
					next_state = copy.deepcopy(stage)
					if rule.tags is not None:
						next_state.tags = next_state.tags | rule.tags
					rule.delta(next_state)
					paths: list[list[str]] = copy.deepcopy(self.lines[stage])
					for path in paths:
						path.append(rule.name)
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

# complete: wen, elder, cannahawk
# partial: ultihawk
# remaining: apelio, lara, sbt, ultinochi, ultirei, ultifalcos, 

playbook: list[Rule] = []

for card in Data.monsters:
	# normal summons
	if card != 'wen':
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
		playbook.append(Rule(
			name = f'{card}_normal',
			tags = None,
			check = check(card),
			delta = delta(card),
		))
	else:
		def check(card: str) -> Callable[[Stage], bool]:
			def check(stage: Stage) -> bool:
				return stage.has('hand', 'wen') and stage.has('exile', card)
			return check
		def delta(card: str) -> Callable[[Stage], None]:
			def delta(stage: Stage) -> None:
				stage.move('hand', 'field', 'wen')
				stage.move('exile', 'field', card)
				stage.normal_summons -= 1
			return delta
		playbook.append(Rule(
			name = f'wen_normal_{card}',
			tags = {f'{card}_special'},
			check = check(card),
			delta = delta(card),
		))
	
	# cannahawk sopt
	if card != 'cannahawk':
		def delta(card: str) -> Callable[[Stage], None]:
			def delta(stage: Stage) -> None:
				stage.add('exile', card)
			return delta
		playbook.append(Rule(
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
		playbook.append(Rule(
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
		playbook.append(Rule(
			name = f'ultihawk_bounce_{tamer}_{beast}',
			tags = {f'{tamer}_special', f'{beast}_special'},
			check = check(tamer, beast),
			delta = delta(tamer, beast),
		))

stage: Stage = Stage()
stage.hand = {'cannahawk': 1, 'elder': 1}
stage.tags = {'cannahawk_deck', 'elder_deck'}
# stage.normal_summons = 2

engine: Engine = Engine(stage, playbook)
engine.compute_combos()
engine.write_combos()
