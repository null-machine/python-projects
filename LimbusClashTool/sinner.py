import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class Sinner:

	def __init__(self, name, skills):
		self.name = name
		self.skills = skills
	
	def gen_summary(self):
		return f'{self.name} | agg: {round(self.min_agg, 2)}~{round(self.max_agg, 2)} | raw: {round(self.min_raw, 2)}~{round(self.max_raw, 2)} @ {round(self.offense, 2)}'
	
	def calibrate(self):
		for i in range(0, len(self.skills)):
			self.skills[i].user = self.name
			self.skills[i].type = f's{i + 1}'
			self.skills[i].calibrate()
		
		plt.style.use('dark_background')
		matplotlib.rcParams['font.family'] = ['DejaVu Sans Mono', 'monospace']
		fig, ax = plt.subplots(3, 1, figsize=(7, 5))
		# plt.figure()
		
		for i in range(0, len(self.skills)):
			breakpoints, max_chance, reg_chance, min_chance, pos_chance, neg_chance = self.skills[i].calibrate()
			if self.skills[i].coin_type == 'minus':
				min_color = '#00ffff'
				max_color = '#ff00ff'
				pos_color = '#e77aff'
				neg_color = '#95d8ff'
			else:
				min_color = '#ff00ff'
				max_color = '#00ffff'
				pos_color = '#95d8ff'
				neg_color = '#e77aff'
			ax[i].step(breakpoints, pos_chance, color=pos_color)
			ax[i].step(breakpoints, neg_chance, color=neg_color)
			ax[i].step(breakpoints, reg_chance, color='#c6aeff')
			ax[i].step(breakpoints, min_chance, color=min_color)
			ax[i].step(breakpoints, max_chance, color=max_color)
			ax[i].set(ylim=(0, 1.1), xlim=(0, 40), yticks=np.arange(0, 1.1, 0.25), xticks=np.arange(0, 40.1, 2))
			ax[i].yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
			ax[i].set_title(self.skills[i].gen_display()) # fontsize=10

		if self.name.endswith('_partial'):
			self.max_agg = (3 * self.skills[0].max_agg + 2 * self.skills[1].max_agg) / 5
			self.min_agg = (3 * self.skills[0].min_agg + 2 * self.skills[1].min_agg) / 5
			self.max_raw = (3 * self.skills[0].max_raw + 2 * self.skills[1].max_raw) / 5
			self.min_raw = (3 * self.skills[0].min_raw + 2 * self.skills[1].min_raw) / 5
			self.offense = (3 * self.skills[0].offense + 2 * self.skills[1].offense) / 5
			
			self.turn_one_max_agg = (9 * self.skills[0].max_agg + 16 * self.skills[1].max_agg) / 25
			self.turn_one_min_agg = (9 * self.skills[0].min_agg + 16 * self.skills[1].min_agg) / 25
			self.turn_one_max_raw = (9 * self.skills[0].max_raw + 16 * self.skills[1].max_raw) / 25
			self.turn_one_min_raw = (9 * self.skills[0].min_raw + 16 * self.skills[1].min_raw) / 25
			self.turn_one_offense = (9 * self.skills[0].offense + 16 * self.skills[1].offense) / 25
		else:
			self.turn_one_max_agg = (1 * self.skills[0].max_agg + 2 * self.skills[1].max_agg + self.skills[2].max_agg) / 6
			self.turn_one_min_agg = (1 * self.skills[0].min_agg + 2 * self.skills[1].min_agg + self.skills[2].min_agg) / 6
			self.turn_one_max_raw = (1 * self.skills[0].max_raw + 2 * self.skills[1].max_raw + self.skills[2].max_raw) / 6
			self.turn_one_min_raw = (1 * self.skills[0].min_raw + 2 * self.skills[1].min_raw + self.skills[2].min_raw) / 6
			self.turn_one_offense = (1 * self.skills[0].offense + 2 * self.skills[1].offense + self.skills[2].offense) / 6
			
			self.max_agg = (3 * self.skills[0].max_agg + 2 * self.skills[1].max_agg + self.skills[2].max_agg) / 6
			self.min_agg = (3 * self.skills[0].min_agg + 2 * self.skills[1].min_agg + self.skills[2].min_agg) / 6
			self.max_raw = (3 * self.skills[0].max_raw + 2 * self.skills[1].max_raw + self.skills[2].max_raw) / 6
			self.min_raw = (3 * self.skills[0].min_raw + 2 * self.skills[1].min_raw + self.skills[2].min_raw) / 6
			self.offense = (3 * self.skills[0].offense + 2 * self.skills[1].offense + self.skills[2].offense) / 6
		
		fig.canvas.manager.set_window_title('Sinner Ultimate Scientific Analysis Model Of Generally Unknown Strategies')
		fig.suptitle(self.gen_summary())
		fig.tight_layout()
		# plt.show()
		
		return plt
