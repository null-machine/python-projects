from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyListener
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import threading
import sys
import os
import time

mouse = MouseController()
global f6_held

f6_held = False

def mouse_drag(ray):
	mouse.press(Button.left)
	mouse.move(ray[0], ray[1])
	mouse.release(Button.left)

def main_loop():
	global f6_held
	step = 0
	distance = 0
	direction = 0
	while True:
		if f6_held and step < 200:
			if direction % 4 == 0:
				if step == 0:
					distance += 1
					mouse_drag((0, -1))
				if step < distance:
					mouse_drag((1, 1))
					step += 1
				else:
					step = 0
					direction = (direction + 1) % 4
			elif direction % 4 == 1:
				if step < distance:
					mouse_drag((-1, 1))
					step += 1
				else:
					step = 0
					direction = (direction + 1) % 4
			elif direction % 4 == 2:
				if step < distance:
					mouse_drag((-1, -1))
					step += 1
				else:
					step = 0
					direction = (direction + 1) % 4
			elif direction % 4 == 3:
				if step < distance:
					mouse_drag((1, -1))
					step += 1
				else:
					step = 0
					direction = (direction + 1) % 4
		else:
			step = 0
			distance = 0
			direction = 0
		time.sleep(0.02)



def placement_micro():
	mouse.move(0, 1)

def on_press(key):
	# print('{0} pressed'.format(key))
	if key == Key.f6:
		global f6_held
		f6_held = True

def on_release(key):
	print('{0} release'.format(key))
	if key == Key.f6:
		mouse.release(Button.left)
		global f6_held
		f6_held = False
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
