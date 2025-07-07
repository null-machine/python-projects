from ahk import AHK
from mss import mss
import cv2
import time
import numpy
import os
import sys
import tkinter

ahk = AHK()
mss = mss()

class Target:
	def __init__(self, name, image, action, offset):
		self.name = name
		self.image = image
		self.action = action
		self.offset = offset

	# time.sleep(numpy.random.uniform(0.05, 0.1))

def click(point, fuzz=4):
	x = point[0] + int(numpy.random.uniform(-fuzz, fuzz + 1))
	y = point[1] + int(numpy.random.uniform(-fuzz, fuzz + 1))
	ahk.click(x=x, y=y, coord_mode='Screen')

def match_template(frame, target, threshold=0.035):
	result = cv2.matchTemplate(frame, target, cv2.TM_SQDIFF_NORMED)
	min_value, max_value, min_point, max_point = cv2.minMaxLoc(result)
	point = (numpy.array([min_point[1],]), numpy.array([min_point[0],]))
	# cv2.imshow("frame", frame)
	# cv2.imshow("target", target)
	# cv2.waitKey(0)
	if min_value < threshold and point[0].size > 0 and point[1].size > 0:
		point = point[1][0] + target.shape[1] / 2, point[0][0] + target.shape[0] / 2
		return point
	else:
		return None

def main_loop():
	files = [file for file in os.listdir() if file.endswith('.png')]
	print(files)
	targets = {file : Target(file, cv2.imread(file), click, (0, 0)) for file in files}
	# targets['3.png'].offset = (0, 50)
	# targets['4.png'].offset = (0, 50)
	# targets['5.png'].offset = (0, 50)
	# targets['to_battle.png'].offset = (0, 50)
	# targets['unselected_sinner.png'].offset = (0, 50)
	# targets['qmark_choice.png'].offset = (50, 80)
	# targets['0win.png'].action = win_action
	# targets['exit.png'].action = exit_action
	
	while True:
		for target in targets.values():
			frame = mss.grab({'top': 0, 'left': 0, 'width': 1920, 'height': 1080})
			frame = numpy.array(frame)
			frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
			point = match_template(frame, target.image)
			if point is not None and target.action:
				print(f'{target.name} found, performing {target.action}')
				target.action(numpy.add(point, target.offset))
		time.sleep(numpy.random.uniform(0.1, 5))

# os.chdir(os.path.dirname(sys.argv[0]))
# main_thread = threading.Thread(target=main_loop)
# main_thread.daemon = True
# main_thread.start()

ahk.add_hotkey('ralt & lalt', callback=lambda: sys.exit())

ahk.start_hotkeys()
# ahk.block_forever()
main_loop()
