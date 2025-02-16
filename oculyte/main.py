import sys
import cv2
import numpy as np
from mss import mss

CARD_MAX_AREA = 120000
CARD_MIN_AREA = 25000

monitor = {
	'top': 0,
	'left': 0,
	'width': 1920,
	'height': 1080,
}
deltaX = 360
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

sct = mss()
image = np.array(sct.grab(monitor))
matrix = cv2.getPerspectiveTransform(input_points, output_points)
perspective_image = cv2.warpPerspective(image, matrix, (screen_width, screen_height), flags=cv2.INTER_LINEAR)
debug = cv2.warpPerspective(image, matrix, (screen_width, screen_height), flags=cv2.INTER_LINEAR)
cv2.imwrite('perspective.jpg', perspective_image)
grayscale_image = cv2.cvtColor(perspective_image, cv2.COLOR_BGR2GRAY)
_, threshold_image = cv2.threshold(grayscale_image, 200, 255, cv2.THRESH_BINARY)
# _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite('threshold.jpg', threshold_image)
contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
boxes = []
for contour in contours:
	box = cv2.boundingRect(contour)
	x, y, w, h = box
	if 2300 < w * h < 2600 and 1.2 < max(w / h, h / w) < 1.5:
		# print(f'{w * h} {max(w / h, h / w)}')
		boxes.append(box)
# 		cv2.rectangle(debug, (x, y), (x + w, y + h), (0, 0, 255), 1)
# cv2.imwrite('boxes.jpg', debug)



offsetX = 300
offsetY = 200
centroids = [ # east south west north
	(screen_width - deltaX, screen_height / 2 - offsetY),
	(screen_width / 2 + offsetX, screen_height),
	(deltaX, screen_height / 2 + offsetY),
	(screen_width / 2 - offsetX, 0),
]
key = 0
for box in boxes:
	x, y, w, h = box
	roi = perspective_image[y:y+h, x:x+w]
	centroid_index = -1
	centroid_distance = sys.maxsize
	x += w / 2
	y += h / 2
	for i in range(4):
		centroid = centroids[i]
		distance = (centroid[0] - x) * (centroid[0] - x) + (centroid[1] - y) * (centroid[1] - y)
		if distance < centroid_distance:
			centroid_index = i
			centroid_distance = distance
	print(f'{centroid_index} {key} ({x}, {y}) {centroids[centroid_index]}')
	if centroid_index == 0:
		if w > h:
			roi = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)
		else:
			roi = cv2.rotate(roi, cv2.ROTATE_180)
	elif centroid_index == 1:
		if w > h:
			roi = cv2.rotate(roi, cv2.ROTATE_90_CLOCKWISE)
	elif centroid_index == 2:
		if w > h:
			roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
	elif centroid_index == 3:
		if w > h:
			roi = cv2.rotate(roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
		else:
			roi = cv2.rotate(roi, cv2.ROTATE_180)
	cv2.imwrite(f'tiles/box_{centroid_index}_{key}.jpg', roi)
	key += 1
