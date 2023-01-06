from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyListener
from pynput.keyboard import Controller as KeyboardController
from PIL import ImageGrab
import cv2
import time
import threading
import numpy
import os
import sys

mouse = MouseController()
keyboard = KeyboardController()

# global ctrlHeld
# ctrlHeld = False

def small_sleep():
	time.sleep(numpy.random.uniform(0.05, 0.1))

def long_sleep():
	time.sleep(numpy.random.uniform(1.11, 1.2))

def sharp_click(point):
	mouse.position = point
	mouse.move(numpy.random.uniform(-2, 2), numpy.random.uniform(-1, 1))
	small_sleep()
	mouse.press(Button.left)
	small_sleep()
	mouse.release(Button.left)
	small_sleep()

def human_type(key):
	keyboard.press(key)
	small_sleep()
	keyboard.release(key)
	small_sleep()

def construct(point, tower, top, mid, bot):
	human_type(tower)
	sharp_click(point)
	sharp_click(point)
	for i in range(0, top):
		human_type('w')
	for i in range(0, mid):
		human_type('v')
	for i in range(0, bot):
		human_type('z')

def solve_infernal():
	long_sleep()
	print("UNGA BUNGA UNGA BUNGA UNGA B-")
	# construct((666, 620), ';', 0, 2, 4)
	construct((666, 565), 'a', 4, 0, 2) # BM island
	construct((666, 290), 'o', 1, 1, 0) # TM island
	construct((1250, 470), 'x', 2, 2, 0) # RM island
	construct((380, 650), 'q', 2, 0, 0) # BL pool
	human_type(Key.space)
	human_type(Key.space)
	construct((960, 680), 'f', 1, 0, 0) # BR island
	# construct((390, 190), 'b', 2, 1, 0) # TL island
	# construct((666, 260), 'h', 0, 1, 1)
	# construct((666, 260), 'm', 1, 1, 0)
	# construct((666, 260), 't', 0, 1, 0)
	# human_type(Key.tab)
	# sharp_click((1150, 300))
	# sharp_click((80, 760))

# tune the threshold parameter lower if it can't find anything, and higher if there are false positives
def click_target(frame, target, offset = (0, 0), threshold = 0.01):
	result = cv2.matchTemplate(frame, target, cv2.TM_SQDIFF_NORMED)
	min_value, max_value, min_point, max_point = cv2.minMaxLoc(result)
	point = (numpy.array([min_point[1],]), numpy.array([min_point[0],]))
	print(round(min_value, 2))
	# cv2.imshow("img", frame)
	# cv2.waitKey(0)
	# cv2.imshow("target", target)
	# cv2.waitKey(0)
	if min_value < threshold and point[0].size > 0 and point[1].size > 0:
		point = point[1][0] + target.shape[1] / 2, point[0][0] + target.shape[0] / 2
		point = (point[0] + offset[0], point[1] + offset[1])
		point = numpy.multiply(point, (1535 / 1920, 863 / 1080))
		sharp_click(point)
		return True
	return False

def main_loop():
	# while True:
	# 	print(mouse.position)
	# 	time.sleep(1)

	files = os.listdir()
	files = [file for file in files if file.endswith('.png')]

	print(files)
	while True:
		frame = ImageGrab.grab()
		frame = numpy.array(frame)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		for file in files:
			target = cv2.imread(file)
			tokens = file.split(' ')
			if len(tokens) > 1 and tokens[0].lstrip('-').isdigit() and tokens[1].lstrip('-').isdigit():
				if click_target(frame, target, (int(tokens[0]), int(tokens[1]))):
					print(file)
					if file.endswith('levelstart.png'):
						solve_infernal()
					break
			else:
				if click_target(frame, target):
					print(file)
					if file.endswith('levelstart.png'):
						solve_infernal()
					break

# kill switch
def on_press(key):
	# global ctrlHeld
	print('{0} pressed'.format(key))
	# if key == Key.ctrl_l or key == Key.ctrl_r:
	# 	ctrlHeld = True
	# 	print("amonugusg")

def on_release(key):
	# global ctrlHeld
	print('{0} release'.format(key))
	if key == Key.f12:
		mouse.release(Button.left)
		return False

def kill_switch():
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
