import matplotlib.pyplot as plt

class Skill:

	def __init__(self, name, user, base_power, coin_count, coin_power, offense):
		self.name = name
		self.user = user
		self.base_power = base_power
		self.coin_count = coin_count
		self.coin_power = coin_power
		self.offense = offense

	def gen_breakpoints(self, enemy_offense, heads_chance):
		# offense_power = (self.offense - enemy_offense) / 5
		offense_power = 0
		effective_base_power = self.base_power + offense_power
		breakpoints = {}
		breakpoints[0] = 1
		breakpoints[effective_base_power] = 1
		for i in range(self.coin_count):
			breakpoints[effective_base_power + i * self.coin_power] = heads_chance ** i
		# breakpoints[effective_base_power + self.coin_power * self.coin_count] = heads_chance ** self.coin_count
		x, y = zip(*breakpoints.items())
		figure, axis = plt.subplots()
		axis.step(x, y)
		axis.set(ylim = (0, 1.1))
		plt.show()
	
	def clash(enemy_skill):
		return
