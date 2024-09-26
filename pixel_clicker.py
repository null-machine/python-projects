
from ahk import AHK
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyListener
from pynput.keyboard import Controller as KeyboardController
import time
import threading
import numpy
import os
import sys

ahk = AHK(executable_path="C:/Program Files/AutoHotkey/v1.1.37.01/AutoHotkeyU64.exe")
mouse = MouseController()
keyboard = KeyboardController()

def frame_sleep():
	time.sleep(numpy.random.uniform(0.05, 0.1))

def small_sleep():
	time.sleep(0.1)

def long_sleep():
	time.sleep(0.5)

def main_loop():
	
	while True:
		print(ahk.pixel_get_color(960, 660))

def on_press(key):
	if key == Key.menu:
		mouse.release(Button.left)
		return False
	print('Key pressed: {0}	Mouse position: {1}'.format(key, mouse.position))

# def on_release(key):
# 	print('Key released: {0} Mouse position: {1}'.format(key, mouse.position))

def kill_switch():
	# with KeyListener(on_press=on_press, on_release=on_release) as listener: listener.join()
	with KeyListener(on_press=on_press) as listener: listener.join()

os.chdir(os.path.dirname(sys.argv[0]))
main_thread = threading.Thread(target=main_loop)
main_thread.daemon = True
kill_thread = threading.Thread(target=kill_switch)
main_thread.start()
kill_thread.start()
kill_thread.join()