import shutil


class Entry:
	
	def __init__(self, line):
		data = line.split(' | ')
		if len(data) < 11:
			print(line)
		self.first_contact = data[0].split()[0]
		self.last_interaction = data[0].split()[1]
		self.score = self.moons_to_score(data[1])
		self.nationality = data[2]
		self.length = data[3]
		self.medium = data[4]
		self.name = data[5]
		self.appeal = data[6]
		self.aspects = data[7].split(', ')
		self.positive = sorted(data[8].split(', '))
		self.neutral = sorted(data[9].split(', '))
		self.negative = sorted(data[10].split(', '))
	
	def __str__(self):
		# return f'{self.name}'
		return f'{self.first_contact} {self.last_interaction} | {self.score_to_moons(self.score)} | {self.nationality} | {self.length} | {self.medium} | {self.name} | {self.appeal} | {', '.join(self.aspects)} | {', '.join(self.positive)} | {', '.join(self.neutral)} | {', '.join(self.negative)}'
	
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

data = sorted(data, key=lambda x: (x.last_interaction, x.score, x.medium), reverse=True)

with open('footpaths-1.txt', 'w', encoding='utf-8') as file:
	for line in data:
		file.write(f'{line}\n')
