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

from image_target import ImageTarget

mouse = MouseController()
keyboard = KeyboardController()
global prev_time
global elapsed_time

def small_sleep():
	time.sleep(numpy.random.uniform(0.05, 0.1))

def long_sleep():
	time.sleep(numpy.random.uniform(1.11, 1.2))

def take_recording():
	keyboard.press(Key.alt)
	keyboard.press(Key.f10)
	keyboard.release(Key.f10)
	keyboard.release(Key.alt)

def sharp_click(point):
	mouse.position = point
	# mouse.move(numpy.random.uniform(-2, 2), numpy.random.uniform(-1, 1))
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

	construct((666, 565), 'a', 4, 0, 2) # BM island
	construct((1250, 470), 'x', 2, 3, 0) # RM island
	construct((960, 680), 'h', 2, 0, 3) # BR island

	# construct((666, 565), 'a', 4, 0, 2) # BM island
	# construct((666, 290), 'e', 4, 0, 1) # TM island
	# construct((960, 680), ';', 0, 2, 3) # BR island
	# construct((90, 470), 'e', 2, 2, 2) # LM island
	# human_type(Key.tab)

	# construct((666, 565), 'a', 4, 0, 2) # BM island
	# construct((960, 680), ';', 0, 2, 3) # BR island
	# construct((666, 290), 'n', 3, 0, 2) # TM island
	# construct((390, 190), 'y', 2, 2, 0) # TL island

	# construct((666, 565), 'a', 4, 0, 2) # BM island
	# construct((90, 470), 'k', 0, 2, 3) # LM island
	# construct((960, 680), ';', 0, 2, 2) # BR island
	# construct((666, 290), 'n', 3, 0, 1) # TM island
	# construct((1250, 470), 'f', 2, 0, 1) # RM island
	# construct((390, 190), '\'', 0, 2, 3) # TL island

	# construct((666, 565), 'a', 4, 0, 2) # BM island
	# construct((90, 470), 'k', 0, 2, 3) # LM island
	# construct((666, 290), '\'', 0, 2, 4) # TM island
	# construct((960, 680), '\'', 0, 0, 0) # BR island
	# construct((960, 190), 'j', 0, 3, 2) # TR pool
	# construct((380, 650), 'j', 0, 3, 2) # BL pool

	# construct((666, 620), ';', 0, 2, 4)
	# construct((380, 650), 'q', 2, 0, 0) # BL pool
	human_type(Key.space)
	human_type(Key.space)
	time.sleep(300)

def find_level():
	long_sleep()
	sharp_click((1070, 780))
	long_sleep()
	sharp_click((430, 460))
	long_sleep()
	sharp_click((500, 330))
	long_sleep()
	sharp_click((1030, 360))

def click_home():
	long_sleep()
	sharp_click((560, 680))

# tune the threshold parameter lower if it can't find anything, and higher if there are false positives
def click_target(frame, target, offset = (0, 0), threshold = 0.01):
	result = cv2.matchTemplate(frame, target, cv2.TM_SQDIFF_NORMED)
	min_value, max_value, min_point, max_point = cv2.minMaxLoc(result)
	point = (numpy.array([min_point[1],]), numpy.array([min_point[0],]))
	# print(round(min_value, 2))
	# cv2.imshow("img", frame) cv2.waitKey(0) cv2.imshow("target", target) cv2.waitKey(0)
	if min_value < threshold and point[0].size > 0 and point[1].size > 0:
		point = point[1][0] + target.shape[1] / 2, point[0][0] + target.shape[0] / 2
		point = (point[0] + offset[0], point[1] + offset[1])
		point = numpy.multiply(point, (1535 / 1920, 863 / 1080))
		sharp_click(point)
		return True
	return False

def main_loop():
	global prev_time
	global elapsed_time
	# while True:
	# 	print(mouse.position)
	# 	time.sleep(1)

	files = [file for file in os.listdir() if file.endswith('.png')] # file[0:-4]
	print(files)
	image_targets = {file : ImageTarget(file, cv2.imread(file), None, (0, 0)) for file in files}
	image_targets['levelstart.png'].action = solve_infernal
	# image_targets['play.png'].action = find_level
	# image_targets['levelfinish.png'].action = click_home
	prev_time = time.monotonic()
	elapsed_time = 0
	while True:
		elapsed_time += time.monotonic() - prev_time
		# if elapsed_time > 1000:
		# 	# take_recording()
		# 	break
		print('Scanning... ({0}s)'.format(round(elapsed_time, 2)))
		prev_time = time.monotonic()
		frame = ImageGrab.grab()
		frame = numpy.array(frame)
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		for image_target in image_targets.values():
			if click_target(frame, image_target.image, image_target.offset):
				print('{0} found'.format(image_target.name))
				if not image_target.action is None:
					image_target.action()
				elapsed_time = 0
				break


def on_press(key):
	print('{0} pressed'.format(key))

def on_release(key):
	print('{0} release'.format(key))
	if key == Key.f12:
		mouse.release(Button.left)
		return False

def kill_switch():
	with KeyListener(on_press=on_press, on_release=on_release) as listener: listener.join()

os.chdir(os.path.dirname(sys.argv[0]))
main_thread = threading.Thread(target=main_loop)
main_thread.daemon = True # slightly cursed
kill_thread = threading.Thread(target=kill_switch)
main_thread.start()
kill_thread.start()
kill_thread.join()
