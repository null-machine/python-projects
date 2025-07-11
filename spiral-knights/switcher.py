from ahk import AHK
import dxcam 
import cv2
import time
import math
import numpy
import os
import sys
import _thread

ahk = AHK()
ahk.set_coord_mode('Mouse', 'Screen')
monitor_shift = 1920
halting = False
switch_mutex = False

def cancel_switch():
	global switch_mutex
	print('shutting off mutex')
	switch_mutex = False

def auto_switch():
	global switch_mutex
	if switch_mutex:
		return
	switch_mutex = True
	while switch_mutex:
		ahk.send('{lbutton down}{rbutton down}{wheelup}{lbutton up}')
		time.sleep(1)
		ahk.send('{wheeldown}{rbutton up}')
	ahk.send('{lbutton up}{rbutton up}')

ahk.add_hotkey('$*-', callback=auto_switch)
ahk.add_hotkey('$*- up', callback=cancel_switch)

def kill():
	global halting
	halting = True
	_thread.interrupt_main()
	ahk.send('{lshift up}{space up}{ctrl up}{a up}{, up}')
	print('--- halt semaphore set ---')

ahk.add_hotkey('ralt & lalt', callback=kill)

ahk.start_hotkeys()
ahk.block_forever()