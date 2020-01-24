import numpy as np
import cv2
import pytesseract
import pyscreenshot as ss
from multiprocessing import Process
#from pynput import keybo1
#import pyautogui as agard, mouse

# keybinds = {}
# mousePos = (1, 1)

def multiprocess(*fns):
	procs = []
	for fn in fns:
		proc = Process(target=fn)
		proc.start()
		procs.append(proc)
	for p in procs:
		p.join()

def parse_screen(bbox=None):
	frame = ss.grab(bbox);
	frame = np.array(frame)
	return frame

def search_template(frame, target, threshold=0.8):
	res = cv2.matchTemplate(frame, target, cv2.TM_CCOEFF_NORMED)
	target = target.shape
	res = np.where(res > threshold)
	if res[0].any() and res[1].any():
		return res[1][0] + target[1] / 2, res[0][0] + target[0] / 2	

def search_pixel(frame, pixel):
	res = np.where(frame == pixel)
	if res[0].any() and res[1].any():
		return res[1][0], res[0][0]

def search_text(frame): # add search numbers later
	return pytesseract.image_to_string(frame, lang='eng')

if __name__ == '__main__':
	print('boo')

'''
def quick_click(frame, target, threshold=0.8):
	print('quick click')
	res = cv2.matchTemplate(frame, target, cv2.TM_CCOEFF_NORMED)
	target = target.shape
	res = np.where(res > threshold)
	if res[0].any() and res[1].any():
		#oldPos = mousePos
		ag.click(res[1][0] + target[1] / 2, res[0][0] + target[0] / 2)
		#ag.move(*oldPos)


def bind_key(key, action, *actionArgs):
	keybinds[key] = action(*actionArgs)

# helper helper functions i guess

def call_key()

def on_press(key):
	if keybinds(button)() is not None:
		keybinds(button)()

def on_click(x, y, button, pressed):
	if pressed and keybinds(button) is not None:
		keybinds(button)()

def on_move(x, y):
	mousePos = (x, y)

#with keyboard.Listener(on_press=on_press) as listener:
with mouse.Listener(on_move=on_move) as listener:
	listener.join()
'''
