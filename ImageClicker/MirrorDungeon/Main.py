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

class ImageTarget:
	def __init__(self, name, image, action, offset):
		self.name = name
		self.image = image
		self.action = action
		self.offset = offset

mouse = MouseController()
keyboard = KeyboardController()

def frame_sleep():
	time.sleep(0.05)

def small_sleep():
	time.sleep(0.1)

def long_sleep():
	time.sleep(0.5)

def click_point(point):
	mouse.position = point
	# frame_sleep()
	mouse.press(Button.left)
	frame_sleep()
	mouse.release(Button.left)
	frame_sleep()

def type_key(key):
	keyboard.press(key)
	frame_sleep()
	keyboard.release(key)
	frame_sleep()

def win_action(point):
	click_point(point)
	# long_sleep()
	click_point((point[0] - 120, point[1] + 20))

def level_action(point):
	click_point(point)
	click_point((1000, 640))
	click_point((900, 640))
	long_sleep()
	click_point((300, 400))
	click_point((1350, 720))
	long_sleep()
	click_point((1000, 640))

def recruit_action(point):
	click_point(point)
	long_sleep()
	long_sleep()
	long_sleep()
	click_point((800, 400))
	click_point((1350, 720))
	click_point((1350, 720))
	click_point((1350, 720))

def choose_sinner_action(point):
	click_point((370, 340)) # yi sang
	click_point((710, 340)) # don quixote
	click_point((370, 570)) # heathcliff
	click_point((710, 570)) # rodion
	click_point((870, 570)) # sinclair
	click_point((870, 340)) # ryoshu
	click_point((1060, 340)) # meursault
	click_point((1060, 570)) # outis
	# click_point(point)
	recruit_action(point)


# def node_action(point):
	# if point[0] < 200:
	# 	mouse.position = (point[0] + 1, point[1] - 100)
	# 	frame_sleep()
	# 	mouse.press(Button.left)
	# 	frame_sleep()
	# 	mouse.position = (point[0] - 1, point[1] - 100)
	# 	frame_sleep()
	# 	mouse.release(Button.left)
	# elif point[0] > 1400:
	# 	mouse.position = (point[0], point[1] - 100)
	# 	frame_sleep()
	# 	mouse.press(Button.left)
	# 	frame_sleep()
	# 	mouse.move(5, 0)
	# 	frame_sleep()
	# 	mouse.move(5, 0)
	# 	frame_sleep()
	# 	mouse.move(1, 0)
	# 	mouse.move(1, 0)
	# 	mouse.move(1, 0)
	# 	mouse.move(1, 0)
	# 	mouse.move(1, 0)
	# 	mouse.release(Button.left)
	# else:
	# click_point(point)
	# use pinned screenshot bars to eliminate side nodes. this is the best solution.

def ego_action(point):
	click_point((480, 360))
	# long_sleep()
	click_point(point)

def match_template(frame, target, offset = (0, 0), threshold = 0.06):
	result = cv2.matchTemplate(frame, target, cv2.TM_SQDIFF_NORMED)
	min_value, max_value, min_point, max_point = cv2.minMaxLoc(result)
	point = (numpy.array([min_point[1],]), numpy.array([min_point[0],]))
	# cv2.imshow("frame", frame) cv2.imshow("target", target) cv2.waitKey(0)
	if min_value < threshold and point[0].size > 0 and point[1].size > 0:
		point = point[1][0] + target.shape[1] / 2, point[0][0] + target.shape[0] / 2
		point = (point[0] + offset[0], point[1] + offset[1])
		point = numpy.multiply(point, (1535 / 1920, 863 / 1080))
		return point
	else:
		return None


def main_loop():
	files = [file for file in os.listdir() if file.endswith('.png')]
	print(files)
	image_targets = {file : ImageTarget(file, cv2.imread(file), click_point, (0, 0)) for file in files}
	image_targets['3.png'].offset = (0, 50)
	image_targets['4.png'].offset = (0, 50)
	image_targets['5.png'].offset = (0, 50)
	image_targets['0win.png'].action = win_action
	image_targets['level_hong_lu.png'].action = level_action
	image_targets['level_gregor.png'].action = level_action
	image_targets['level_faust.png'].action = level_action
	# image_targets['select_sinner.png'].action = recruit_action
	image_targets['select_ego.png'].action = ego_action
	image_targets['choose_sinner.png'].action = choose_sinner_action
	# image_targets['node.png'].action = node_action
	

	prev_time = time.monotonic()
	elapsed_time = 0
	while True:
		elapsed_time += time.monotonic() - prev_time
		# if elapsed_time >= 10:
		# 	print('Scanning... ({0}s)'.format(round(elapsed_time, 2)))
		prev_time = time.monotonic()
		for image_target in image_targets.values():
			frame = ImageGrab.grab()
			frame = numpy.array(frame)
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			point = match_template(frame, image_target.image, image_target.offset)
			if point is not None and image_target.action:
				print('{0} found, performing {1}'.format(image_target.name, image_target.action))
				image_target.action(numpy.add(point, image_target.offset))
				elapsed_time = 0


def on_press(key):
	if key == Key.menu:
		mouse.release(Button.left)
		return False
	print('Key pressed: {0}	Mouse position: {1}'.format(key, mouse.position))

def on_release(key):
	print('Key released: {0} Mouse position: {1}'.format(key, mouse.position))

def kill_switch():
	with KeyListener(on_press=on_press, on_release=on_release) as listener: listener.join()

os.chdir(os.path.dirname(sys.argv[0]))
main_thread = threading.Thread(target=main_loop)
main_thread.daemon = True
kill_thread = threading.Thread(target=kill_switch)
main_thread.start()
kill_thread.start()
kill_thread.join()
