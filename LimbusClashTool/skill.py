# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom

class Skill:

	def __init__(self, name, user, base_power, coin_count, coin_power, offense):
		self.name = name
		self.user = user
		self.base_power = base_power
		self.coin_count = coin_count
		self.coin_power = coin_power
		self.offense = offense

	def gen_breakpoints(self, enemy_offense):
		offense_power = (self.offense - enemy_offense) / 5
		# offense_power = 0
		effective_base_power = self.base_power + offense_power
		breakpoints = []
		min_chance = []
		reg_chance = []
		max_chance = []
		breakpoints.append(0)
		min_chance.append(1)
		reg_chance.append(1)
		max_chance.append(1)
		for i in range(self.coin_count + 1):
			breakpoints.append(effective_base_power + i * self.coin_power)
			# min_chance.append(0.3 ** i)
			# reg_chance.append(0.5 ** i)
			# max_chance.append(0.7 ** i)
			min_chance.append(self.eval_chance(0.3, i))
			reg_chance.append(self.eval_chance(0.5, i))
			max_chance.append(self.eval_chance(0.7, i))
		plt.style.use('dark_background')
		fig, ax = plt.subplots()
		ax.step(breakpoints, min_chance, color='magenta')
		ax.step(breakpoints, reg_chance, color='yellow')
		ax.step(breakpoints, max_chance, color='cyan')
		ax.set(ylim = (0, 1.1))
		fig.canvas.manager.set_window_title('Sinner Ultimate Scientific Analysis Model Of Generally Unknown Strategies')
		plt.title(f'{self.user}: {self.name}')
		plt.xlabel('power of an enemy skill with zero offense that always rolls the same')
		plt.ylabel('chance of winning on any coin in the clash')
		# print(binom.cdf(6, 13, 0.6))
		# print(binom.cdf(3 - 1, 3, 0.5))
		plt.show()
	
	def eval_chance(self, heads_chance, required_heads):
		if required_heads <= 0:
			return 1
		chance = 0
		coins_remaining = self.coin_count
		while coins_remaining >= required_heads:
			k = coins_remaining - required_heads
			chance += (1 - chance) * (binom.cdf(k, coins_remaining, 1 - heads_chance))
			coins_remaining -= 1
		return chance
	
	def clash(enemy_skill):
		return
