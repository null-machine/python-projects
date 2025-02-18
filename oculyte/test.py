from pathlib import Path
import cv2

# for i in range (1, 10):
# 	background = cv2.imread(f'bank/{i}p.png')
# 	template = cv2.imread('tiles/box_1_47.jpg')
# 	background = cv2.blur(background, (2, 2))
# 	# cv2.imshow('a', background)
# 	# cv2.waitKey(0)

# 	result = cv2.minMaxLoc(cv2.matchTemplate(background, template, cv2.TM_SQDIFF))[0]
# 	print(result)

paths = Path('bank')
for path in paths.iterdir():
	path = str(path).replace('\\', '/')
	# path = f'./{path}'
	print(path)
	background = cv2.imread(path)
	# background = cv2.resize(background, (0, 0), fx=1.1, fy=1.1)
	background = cv2.copyMakeBorder(background, 5, 5, 5, 5, cv2.BORDER_REPLICATE)
	cv2.imwrite(path, background)
	