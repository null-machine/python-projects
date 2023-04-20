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
	# time.sleep(numpy.random.uniform(0.0625, 0.125))
	
	return

def long_sleep():
	time.sleep(numpy.random.uniform(1.11, 1.2))

def take_recording():
	keyboard.press(Key.alt)
	keyboard.press(Key.f10)
	keyboard.release(Key.f10)
	keyboard.release(Key.alt)

def click_point(point):
	mouse.position = point
	small_sleep()
	mouse.press(Button.left)
	small_sleep()
	mouse.release(Button.left)
	small_sleep()

def type_key(key):
	keyboard.press(key)
	small_sleep()
	keyboard.release(key)
	small_sleep()

def select_time():
	click_point((850, 600))
	click_point((850, 600))
	click_point((850, 600))
	click_point((760, 770))
	click_point((930, 720))
	time.sleep(0.3)

def main_loop():
	return

def on_press(key):
	print('Key pressed: {0}	Mouse position: {1}'.format(key, mouse.position))

def on_release(key):
	if key == Key.menu:
		mouse.release(Button.left)
		return False
	elif key == Key.ctrl_r:
		select_time()

def kill_switch():
	with KeyListener(on_press=on_press, on_release=on_release) as listener: listener.join()

os.chdir(os.path.dirname(sys.argv[0]))
main_thread = threading.Thread(target=main_loop)
main_thread.daemon = True
kill_thread = threading.Thread(target=kill_switch)
main_thread.start()
kill_thread.start()
kill_thread.join()