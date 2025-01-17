
class Board:
	def __init__(self, new_round_data):
		self.tiles = {
			'1z': 4, '2z': 4, '3z': 4, '4z': 4, '5z': 4, '6z': 4, '7z': 4,
			'1s': 4, '2s': 4, '3s': 4, '4s': 4, '5s': 4, '6s': 4, '7s': 4, '8s': 4, '9s': 4,
			'1p': 4, '2p': 4, '3p': 4, '4p': 4, '5p': 4, '6p': 4, '7p': 4, '8p': 4, '9p': 4,
			'1m': 4, '2m': 4, '3m': 4, '4m': 4, '5m': 4, '6m': 4, '7m': 4, '8m': 4, '9m': 4,
		}
		for tile in new_round_data['tiles']:
			self.tiles[tile] -= 1
		# self.seat = new_round_data['seat']
		self.last_discard = None
		print(f'\n{self.tiles}')
	
	def parse_discard(self, data):
		self.tiles[data['tile']] -= 1
		self.last_discard = data['tile']
		print(f'\n{self.tiles}')
	
	def parse_meld(self, data):
		if last_discard is not None:
			self.tiles[self.last_discard] += 1
		for tile in data.tiles:
			self.tiles[tile] -= 1
		print(f'\n{self.tiles}')