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

def small_sleep():
	time.sleep(numpy.random.uniform(0.05, 0.1))

def long_sleep():
	time.sleep(numpy.random.uniform(1.11, 1.2))

def click_point(point):
	mouse.position = point
	mouse.move(numpy.random.uniform(-24, 24), numpy.random.uniform(-11, 11))
	small_sleep()
	mouse.press(Button.left)
	small_sleep()
	mouse.release(Button.left)
	# small_sleep()
	long_sleep()

def type_key(key):
	keyboard.press(key)
	small_sleep()
	keyboard.release(key)
	small_sleep()

def match_template(frame, target, offset = (0, 0), threshold = 0.05):
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
	image_targets['level_start.png'].offset = (40, 0)
	image_targets['done.png'].offset = (200, 0)

	prev_time = time.monotonic()
	elapsed_time = 0
	while True:
		elapsed_time += time.monotonic() - prev_time
		prev_time = time.monotonic()
		frame = ImageGrab.grab()
		frame = numpy.array(frame)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		for image_target in image_targets.values():
			point = match_template(frame, image_target.image, image_target.offset)
			if point is not None and image_target.action:
				print('{0} found'.format(image_target.name))
				image_target.action(numpy.add(point, image_target.offset))
				time.sleep(0.75)
				elapsed_time = 0
				break


def on_press(key):
	print('Key pressed: {0}    Mouse position: {1}'.format(key, mouse.position))

def on_release(key):
	print('Key released: {0}    Mouse position: {1}'.format(key, mouse.position))
	if key == Key.menu:
		mouse.release(Button.left)
		return False

def kill_switch():
	with KeyListener(on_press=on_press, on_release=on_release) as listener: listener.join()

os.chdir(os.path.dirname(sys.argv[0]))
main_thread = threading.Thread(target=main_loop)
main_thread.daemon = True
kill_thread = threading.Thread(target=kill_switch)
main_thread.start()
kill_thread.start()
kill_thread.join()
