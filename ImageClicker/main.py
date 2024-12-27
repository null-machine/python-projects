import cv2
import numpy as np
from mss import mss

monitor = {
	'top': 0,
	'left': 0,
	'width': 1920,
	'height': 1080,
}

with mss() as sct:
	input_points = np.float32([
		[600, 150],
		[1320, 150],
		[1460, 740],
		[450, 740],
	])
	output_points = np.float32([
		[0, 0],
		[900, 0],
		[900, 900],
		[0, 900],
	])
	img = np.array(sct.grab(monitor))
	mat = cv2.getPerspectiveTransform(input_points, output_points)
	out = cv2.warpPerspective(img, mat, (900, 900), flags=cv2.INTER_LINEAR)
	# cv2.imwrite('output.jpg', out)
	cv2.imshow('output', out)
	cv2.waitKey(0)
	

# img = ImageGrab.grab()


# table_points = np.float32([pt_A, pt_B, pt_C, pt_D])
# output_points = np.float32([])

# img = cv2.imread('sample.jpg')