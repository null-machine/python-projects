
class Board:
	def __init__(self):
		self.tiles = {
			'z1': 4, 'z2': 4, 'z3': 4, 'z4': 4, 'z5': 4, 'z6': 4, 'z7': 4,
			's1': 4, 's2': 4, 's3': 4, 's4': 4, 's5': 4, 's6': 4, 's7': 4, 's8': 4, 's9': 4,
			'p1': 4, 'p2': 4, 'p3': 4, 'p4': 4, 'p5': 4, 'p6': 4, 'p7': 4, 'p8': 4, 'p9': 4,
			'm1': 4, 'm2': 4, 'm3': 4, 'm4': 4, 'm5': 4, 'm6': 4, 'm7': 4, 'm8': 4, 'm9': 4,
		}
		discard_piles = []
		revealed_piles = []
	
	def parse(self, name, data):
		