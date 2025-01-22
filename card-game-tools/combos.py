
# the loop
# start from a board state
# generate possible moves
# for each move, generate another board state
# 


class Data:
	
	def __init__(self):
		
		# spells
		self.shinra = False
		self.solo = [ False, False ] # present
		
		# vaylantz, sss regular hshift
		self.priestess = [ False, False, False ]
		self.archer = [ False, False, False ]
		self.ninja = [ False, False, False ]
		self.baron = [ False, False, False ]
		self.viscount = [ False, False, False ]
		self.marquess = [ False, False, False ]
		self.dominator = [ False, False, False ]
		
		# fuse, sss or hshift
		self.genesis = False
		self.arktos = False
		
		self.attack = 0
		self.steps = 0
		self.draw = 0
		
		self.pops = 0
		self.punts = 0
		
		