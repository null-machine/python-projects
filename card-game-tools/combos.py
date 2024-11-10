


class Data:
	
	def __init__(self):
		
		# occupancy, true when occupied
		self.extra_monster_zones = [ False, False ]
		self.monster_zones = [ False, False, False, False, False ]
		self.backrow_zones = [ False, False, False, False, False ]
		self.field_zones = [ False, False ]
		
		# spells
		self.shinra = [ False, False ] # present, used
		self.konig = False # present
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
		
		