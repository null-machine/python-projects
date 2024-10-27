


class Entry:
	
	def __init__(self, line):
		data = line.split(' | ')
		self.timeframe = data[0]
		self.score = self.moons_to_score(data[1])
		self.medium = data[2]
		self.length = data[3]
		self.name = data[4] # ⌚
			# quick is like two hours
			# short is like psycholonials
			# medium is like a seasonal anime
			# long is like homestuck
		self.appeal = data[5]
		self.aspects = data[6].split(', ')
		self.tags = sorted(data[7].split(', '))
		self.warnings = sorted(data[8].split(', '))
	
	def __str__(self):
		string = f'{self.timeframe} | {self.medium} |  | {self.score_to_moons(self.score)} | {self.name} | {self.appeal} | {', '.join(self.aspects)} | {', '.join(self.tags)} | {', '.join(self.warnings)}'
		return string
	
	def moons_to_score(self, moons):
		return moons.count('🌕') * 4 + moons.count('🌖') * 3 + moons.count('🌗') * 2 + moons.count('🌘')
	
	def score_to_moons(self, score):
		moons = ''
		for i in range(0, int(score / 4)):
			moons += '🌕'
		if score % 4 == 3:
			moons += '🌖'
		elif score % 4 == 2:
			moons += '🌗'
		elif score % 4 == 1:
			moons += '🌘'
		for i in range(0, 6 - len(moons)):
			moons += '🌑'
		return moons

data = []

with open('footpaths.txt', encoding='utf-8') as file:
	for line in file:
		line = line.strip()
		if line:
			data.append(Entry(line))

data = sorted(data, key=lambda x: (x.medium, -x.score))

with open('footpaths.txt', 'w', encoding='utf-8') as file:
	for line in data:
		file.write(f'{line}\n')