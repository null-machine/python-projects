

class Stage:
	
	def __init__(
		self,
		*,
		hand: dict[str, int] = {},
		deck: dict[str, int] = {},
		field: dict[str, int] = {},
		grave: dict[str, int] = {},
		exile: dict[str, int] = {},
		tags: set[str] = set(),
		normal_summons: int = 1,
	) -> bool:
		self.piles = [hand, deck, field, grave, exile]
		self.pile_lookup = {'hand': 0, 'deck': 1, 'field': 2, 'grave': 3, 'exile': 4}
		self.tags = tags
		self.normal_summons = normal_summons
	
	def __eq__(self, other):
		# return (self.hand == other.hand and
		# 	self.field == other.field and
		# 	self.grave == other.grave and
		# 	self.exile == other.exile and
		# 	self.normal_summons == other.normal_summons)
		return self.piles == other.piles
	
	def __hash__(self):
		# data = {
		# 	'hand': self.hand,
		# 	'field': self.field,
		# 	'grave': self.grave,
		# 	'exile': self.exile,
		# 	'tags': sorted(self.tags),
		# 	'normal_summons': self.normal_summons,
		# }
		# return hash(json.dumps(data, sort_keys=True))
		return hash(json.dumps(self.piles, sort_keys=True))
		
	
	def has(self, pile_name: str, card: str) -> bool:
		# pile_name = getattr(self, pile_name)
		pile = self.piles[self.pile_lookup[pile_name]]
		return card in pile and pile[card] > 0
	
	def add(self, pile_name: str, card: str) -> None:
		# pile_name = getattr(self, pile_name)
		pile = self.piles[self.pile_lookup[pile_name]]
		pile[card] = pile.get(card, 0) + 1
	
	def remove(self, pile_name: str, card: str) -> None:
		# pile_name = getattr(self, pile_name)
		pile = self.piles[self.pile_lookup[pile_name]]
		pile[card] = pile[card] - 1
		if pile[card] <= 0:
			pile.pop(card)
	
	def move(self, source: str, output: str, card: str) -> None:
		self.remove(source, card)
		self.add(output, card)
	
	def to_string(self):
		data = []
		if self.piles[0]:
			data.append(f'Field: {self.piles[0]}')
		if self.piles[2]:
			data.append(f'Hand: {self.piles[2]}')
		if self.piles[3]:
			data.append(f'Grave: {self.piles[3]}')
		if self.piles[4]:
			data.append(f'Exile: {self.piles[4]}')
		# if self.tags:
		# 	data.append(f'{self.tags}')
		return ' | '.join(data)