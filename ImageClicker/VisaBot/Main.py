# target naming scheme: `[x offset] [y offset] [image name].png`
# example: `-20 50 start.png` will click 20 pixels to the left and
# 50 pixels beneath the center of start.png when it is found onscreen.

# this bot scans its working directory for png files as targets.
# when it finds a target onscreen, it will click it, with respect to offset.
# if no offset is found, it will click its center.

# offset is in pixels; x from left to right, and y from up to down.
# both are relative to the center of each target's screenshot.

# pressing escape terminates the bot.


from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyListener
from PIL import ImageGrab
import cv2
import time
import threading
import numpy
import os
import sys

mouse = MouseController()

# tune the threshold parameter lower if it can't find anything, and higher if there are false positives
def click_target(frame, target, offset=(0, 0), threshold=0.9):
	result = cv2.matchTemplate(frame, target, cv2.TM_SQDIFF_NORMED)
	min_value, max_value, min_point, max_point = cv2.minMaxLoc(result)
	point = (numpy.array([min_point[1],]), numpy.array([min_point[0],]))
	print(min_value)
	# cv2.imshow("img", frame)
	# cv2.waitKey(0)
	# cv2.imshow("target", target)
	# cv2.waitKey(0)
	if min_value < 1 - threshold and point[0].size > 0 and point[1].size > 0:
		point = point[1][0] + target.shape[1] / 2, point[0][0] + target.shape[0] / 2
		point = (point[0] + offset[0], point[1] + offset[1])
		human_click(point)

		return True
	return False

def human_click(point):
	moveTime = numpy.linalg.norm(numpy.array(point) - numpy.array(mouse.position)) / numpy.linalg.norm((1535, 863))
	mouse.position = numpy.multiply(point, (1535 / 1920, 863 / 1080)) # thank you pynput
	mouse.move(numpy.random.uniform(-48, 48), numpy.random.uniform(-24, 24))
	mouse.press(Button.left)
	time.sleep(numpy.random.uniform(0.3, 0.5))
	mouse.release(Button.left)
	time.sleep(numpy.random.uniform(0.7, 0.8))

def main_loop():
	files = os.listdir()
	files = [file for file in files if file.endswith('.png')]
	print(files)
	while True:
		frame = ImageGrab.grab()
		frame = numpy.array(frame)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		for file in files:
			# target = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
			target = cv2.imread(file)
			tokens = file.split(' ')
			if len(tokens) > 1 and tokens[0].lstrip('-').isdigit() and tokens[1].lstrip('-').isdigit():
				if click_target(frame, target, (int(tokens[0]), int(tokens[1]))):
					print(file)
					break
			else:
				if click_target(frame, target):
					print(file)
					break

# kill switch
def on_press(key):
	print('{0} pressed'.format(
	key))

def on_release(key):
	print('{0} release'.format(
	key))
	if key == Key.esc:
		mouse.release(Button.left)
		# stop listener
		return False

def kill_switch():
	# collect events until released
	with KeyListener(on_press=on_press, on_release=on_release) as listener:
		listener.join()

# in case we run from cmd
os.chdir(os.path.dirname(sys.argv[0]))

main_thread = threading.Thread(target=main_loop)
main_thread.daemon = True # slightly cursed
kill_thread = threading.Thread(target=kill_switch)
main_thread.start()
kill_thread.start()
kill_thread.join()
