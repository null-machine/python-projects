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
	# time.sleep(numpy.random.uniform(0.9))
	time.sleep(0.5)

def click_point(point):
	mouse.position = point
	frame_sleep()
	mouse.press(Button.left)
	frame_sleep()
	mouse.release(Button.left)
	long_sleep()
	# frame_sleep()

def type_key(key):
	keyboard.press(key)
	frame_sleep()
	keyboard.release(key)
	frame_sleep()

def match_template(frame, target, offset = (0, 0), threshold = 0.01):
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
	
def confirm_delete(point):
	click_point(point)
	time.sleep(1)
	type_key('L')
	type_key('i')
	type_key('m')
	type_key('b')
	type_key('u')
	type_key('s')
	type_key('C')
	type_key('o')
	type_key('m')
	type_key('p')
	type_key('a')
	type_key('n')
	type_key('y')
	type_key(Key.enter)

def ball_click(point):
	for i in range(0, 6):
		click_point(point)
		long_sleep()

def main_loop():
	files = [file for file in os.listdir() if file.endswith('.png')]
	print(files)
	image_targets = {file : ImageTarget(file, cv2.imread(file), click_point, (0, 0)) for file in files}
	image_targets['limbusinput.png'].action = confirm_delete
	image_targets['ball.png'].offset = (-70, 120)
	image_targets['ball.png'].action = ball_click
	image_targets['fulllunacy.png'].offset = (230, -10)
	# image_targets['standard.png'].offset = (30, 0)

	prev_time = time.monotonic()
	elapsed_time = 0
	while True:
		elapsed_time += time.monotonic() - prev_time
		print('Scanning... ({0}s)'.format(round(elapsed_time, 2)))
		prev_time = time.monotonic()
		frame = ImageGrab.grab()
		frame = numpy.array(frame)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		for image_target in image_targets.values():
			point = match_template(frame, image_target.image, image_target.offset)
			if point is not None and image_target.action:
				print('{0} found, performing {1}'.format(image_target.name, image_target.action))
				image_target.action(numpy.add(point, image_target.offset))
				elapsed_time = 0
				break


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