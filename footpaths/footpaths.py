import shutil


class Entry:
	
	def __init__(self, line):
		data = line.split(' | ')
		self.timeframe = data[0]
		self.score = self.moons_to_score(data[1])
		self.length = data[2]
		self.medium = data[3]
		self.name = data[4]
		self.aspects = data[5].split(', ')
		self.positive = sorted(data[6].split(', '))
		self.neutral = sorted(data[7].split(', '))
		self.negative = sorted(data[8].split(', '))
	
	def __str__(self):
		return f'{self.timeframe} | {self.score_to_moons(self.score)} | {self.length} | {self.medium} | {self.name} | {', '.join(self.aspects)} | {', '.join(self.positive)} | {', '.join(self.neutral)} | {', '.join(self.negative)}'
	
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

shutil.copyfile('footpaths.txt', 'footpaths.txt.backup')

data = []

with open('footpaths.txt', encoding='utf-8') as file:
	for line in file:
		line = line.strip()
		if line:
			data.append(Entry(line))

data = sorted(data, key=lambda x: (x.timeframe, x.medium, x.score), reverse=True)

with open('footpaths.txt', 'w', encoding='utf-8') as file:
	for line in data:
		file.write(f'{line}\n')