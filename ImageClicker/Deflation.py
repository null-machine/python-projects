
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



def main_loop():
	print("UNGA BUNGA UNGA BUNGA UNGA BUNGA UNGA BUNGA UNGA BUNGA UNGA BUNGA UNGA BUNGA UN-")
	time.sleep(3)

	construct((1250, 450), ';', 0, 2, 4)
	construct((670, 565), 'a', 4, 0, 2)
	human_type(Key.space)
	human_type(Key.space)


	while True:
		print(mouse.position)
		time.sleep(1)

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
