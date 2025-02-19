import sys
import numpy as np
import cv2

class Recognizer:
	
	def __init__(self):
		self.references = []
		self.tile_names = [
			'1p', '2p', '3p', '4p', '5p', 'p6', '7p', '8p', '9p',
			'1s', '2s', '3s', '4s', '5s', 's6', '7s', '8s', '9s',
			'1m', '2m', '3m', '4m', '5m', 'm6', '7m', '8m', '9m',
			'1z', '2z', '3z', '4z', '5z', 'z6', '7z',
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