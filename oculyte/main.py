import sys
import cv2
import numpy as np
# from mss import mss
from recognizer import Recognizer

monitor = {
	'top': 0,
	'left': 0,
	'width': 1920,
	'height': 1080,
}
deltaX = 362
deltaY = 125
input_points = np.float32([
	[0, 0],
	[1920, 0],
	[1920, 1080],
	[0, 1080],
])
output_points = np.float32([
	[0, 0],
	[1920, 0],
	[1920 - deltaX, 1080 + deltaY],
	[deltaX, 1080 + deltaY],
])
screen_width = 1920
screen_height = 1080 + deltaY
kernel = np.ones((3, 3), np.uint8)

# sct = mss()
# image = np.array(sct.grab(monitor))
image = cv2.imread('mpc-hc64_a9Hw98DJ6V.png')
matrix = cv2.getPerspectiveTransform(input_points, output_points)
perspective_image = cv2.warpPerspective(image, matrix, (screen_width, screen_height), flags=cv2.INTER_LINEAR)
debug = cv2.warpPerspective(image, matrix, (screen_width, screen_height), flags=cv2.INTER_LINEAR)
# cv2.imwrite('perspective.jpg', perspective_image)
grayscale_image = cv2.cvtColor(perspective_image, cv2.COLOR_BGR2GRAY)
_, threshold_image = cv2.threshold(grayscale_image, 200, 255, cv2.THRESH_BINARY)
# _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# cv2.imwrite('threshold.jpg', threshold_image)
contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
boxes = []
for contour in contours:
	box = cv2.boundingRect(contour)
	x, y, w, h = box
	if 2300 < w * h < 2600 and 1.2 < max(w / h, h / w) < 1.5 and not (1360 < x < 1400 and 140 < y < 180):
		# print(f'{w * h} {max(w / h, h / w)}')
		boxes.append(box)
		cv2.rectangle(debug, (x, y), (x + w, y + h), (0, 0, 255), 1)



image_height, image_width = threshold_image.shape
centroid_offset_x = 10
centroid_offset_y = 10
centroid_padding_x = 550
centroids = [ # east south west north
	(centroid_padding_x, int(image_height / 2) + centroid_offset_y), # west
	(int(image_width / 2) - centroid_offset_x, 200), # north
	(image_width - centroid_padding_x, int(image_height / 2) - centroid_offset_y), # east
	(int(image_width / 2) + centroid_offset_x, 1030), # south
]

for centroid in centroids:
	debug = cv2.circle(debug, (centroid[0], centroid[1]), 10, (0, 0, 255), -1)

recognizer = Recognizer()

discards = [
	[0] * 34,
	[0] * 34,
	[0] * 34,
	[0] * 34,
]
wall = [4] * 34

key = 0
for box in boxes:
	x, y, w, h = box
	centroid_index = -1
	centroid_distance = sys.maxsize
	for i in range(4):
		centroid = centroids[i]
		distance_x = centroid[0] - (x + w / 2)
		distance_y = centroid[1] - (y + h / 2)
		distance = distance_x * distance_x + distance_y * distance_y
		if distance < centroid_distance:
			centroid_index = i
			centroid_distance = distance
	cv2.line(debug, centroids[centroid_index], (x + int(w / 2), y + int(h / 2)), (0, 0, 255), 1)
	# print(f'{centroid_index} {key} ({x}, {y}) {centroids[centroid_index]}')
	
	# if centroid_index == 0:
	# 	if w > h:
	# 		x += 1
	# 		y += 0
	# 	else:
	# 		x += 2
	# 		y += 4
	# elif centroid_index == 1:
	# 	if w > h:
	# 		x += 0
	# 		y += 0
	# 	else:
	# 		x += 0
	# 		y += 0
	# elif centroid_index == 2:
	# 	if w > h:
	# 		x += 0
	# 		y += 0
	# 	else:
	# 		x += 0
	# 		y += 0
	# elif centroid_index == 3:
	# 	if w > h:
	# 		x += 0
	# 		y += 0
	# 	else:
	# 		x += 0
	# 		y += 0
	
	if w > h:
		roi = perspective_image[y:y+36, x:x+48]
	else:
		roi = perspective_image[y:y+48, x:x+36]
	
	roi = perspective_image[y:y+h, x:x+w]
	
	if centroid_index == 0:
		if w > h:
			roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
	elif centroid_index == 1:
		if w > h:
			roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
		else:
			roi = cv2.rotate(roi, cv2.ROTATE_180)
	elif centroid_index == 2:
		if w > h:
			roi = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)
		else:
			roi = cv2.rotate(roi, cv2.ROTATE_180)
	elif centroid_index == 3:
		if w > h:
			roi = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)
	roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	
	tile_key = recognizer.recognize(roi)
	wall[tile_key] -= 1

	if (
		centroid_index == 0 and x + w / 2 > centroid_padding_x or
		centroid_index == 1 and y + h / 2 > 200 or
		centroid_index == 2 and x + w / 2 < image_width - centroid_padding_x or
		centroid_index == 3 and y + h / 2 < 1000
	):
		discards[centroid_index][tile_key] += 1
	cv2.putText(debug, f'{recognizer.tile_names[tile_key]}', (x + int(w / 2) - 16, y + int(h / 2) + 4), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75, color=(255, 255, 255), thickness=6)
	cv2.putText(debug, f'{recognizer.tile_names[tile_key]}', (x + int(w / 2) - 16, y + int(h / 2) + 4), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75, color=(0, 0, 0), thickness=2)
	key += 1

cv2.imwrite('debug.png', debug)
print(discards[0])
print(discards[1])
print(discards[2])
print(discards[3])
print(wall)

full_blanks = [True] * 34
safe_on_interval = [
	[[False] * 9, [False] * 9, [False] * 9],
	[[False] * 9, [False] * 9, [False] * 9],
	[[False] * 9, [False] * 9, [False] * 9],
]

for i in range(3): # for i in range(4):
	for j in range(3):
		for k in range(9):
			discard_index = j * 9 + k
			if discards[i][discard_index] > 0:
				safe_on_interval[i][j][k] = True
				if k < 3 and discards[i][discard_index + 6] > 0:
					safe_on_interval[i][j][k + 3] = True
				elif k < 6:
					safe_on_interval[i][j][k - 3] = True
					safe_on_interval[i][j][k + 3] = True

print(safe_on_interval[0])
print(safe_on_interval[1])
print(safe_on_interval[2])

suits = ['p', 's', 'm']
for player in safe_on_interval:
	output = ''
	for i in range(3):
		for j in range(9):
			if not player[i][j]:
				output += f'{j + 1}'
		output += f'{suits[i]} '
	print(output)
# 	for suit in player: