import sys
import numpy as np
import cv2

class Recognizer:
	
	def __init__(self):
		self.references = []
		self.tile_names = [
			'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9',
			's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9',
			'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9',
			'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7',
		]
		self.channel_length = -1
		kernel = (2, 2)
		for i in ['p', 's', 'm', 'z']:
			for j in range(1, 10):
				if i == 'z' and j > 7:
					break
				reference = cv2.imread(f'bank/{j}{i}.png', cv2.IMREAD_GRAYSCALE)
				# reference = cv2.imread(f'bank/{j}{i}.png', cv2.IMREAD_UNCHANGED)
				reference = cv2.blur(reference, kernel)
				# if self.channel_length != len(reference):
				# 	if self.channel_length == -1:
				# 		self.channel_length = len(reference)
				# 	else:
				# 		print('[W] Reference images have inconsistent channel length')
				self.references.append(reference)
			else:
				continue
			break
	
	def recognize(self, template) -> int:
		min_value = sys.maxsize
		min_key = -1
		for i in range(0, len(self.references)):
			# print(len(self.references[i]), len(template))
			value = cv2.matchTemplate(self.references[i], template, cv2.TM_SQDIFF)
			value = cv2.minMaxLoc(value)[0]
			if value < min_value:
				min_value = value
				min_key = i
		return min_key