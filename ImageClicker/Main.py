# target naming scheme: `[x offset] [y offset] [image name].png`
# example target: `0 0 start.png`

# this bot scans its working directory for properly named png files as targets.
# when it finds a target onscreen, it will click at it, with respect to offset.

# offset is in pixels; x from left to right, and y from up to down.
# both are relative to the center of each target's screenshot.

# pressing escape terminates the bot.


import pyautogui
import time
from pynput.keyboard import Key, Listener
import threading
import cv2
from PIL import ImageGrab
import numpy
import os
import sys

# increasing y lowers click point
def click_target(frame, target, offset = (0, 0), threshold=0.8):
	point = cv2.matchTemplate(frame, target, cv2.TM_CCOEFF_NORMED)
	point = numpy.where(point > threshold)
	if point[0] and point[1]:
		point = point[1][0] + target.shape[1] / 2, point[0][0] + target.shape[0] / 2
		point = (point[0] + offset[0], point[1] + offset[1])
		human_click(point)

def human_click(point):
	moveTime = numpy.linalg.norm(numpy.array(point) - numpy.array(pyautogui.position())) / numpy.linalg.norm(pyautogui.size())
	pyautogui.moveTo(point[0], point[1], moveTime * numpy.random.uniform(0.4, 0.5))
	pyautogui.mouseDown()
	time.sleep(numpy.random.uniform(0, 0.3))
	pyautogui.mouseUp()
	time.sleep(numpy.random.uniform(0, 0.2))

def main_loop():
	frame = ImageGrab.grab()
	frame = numpy.array(frame)
	print(os.listdir())
	target = cv2.imread('0.png')
	click_target(frame, target)

# kill switch
def on_press(key):
	print('{0} pressed'.format(
	key))

def on_release(key):
	print('{0} release'.format(
	key))
	if key == Key.esc:
		# stop listener
		return False

def kill_switch():
	# collect events until released
	with Listener(on_press=on_press, on_release=on_release) as listener:
		listener.join()

# in case we run from cmd
os.chdir(os.path.dirname(sys.argv[0]))

pyautogui.FAILSAFE = False

main_thread = threading.Thread(target=main_loop)
main_thread.daemon = True # slightly cursed
kill_thread = threading.Thread(target=kill_switch)
main_thread.start()
kill_thread.start()
kill_thread.join()
