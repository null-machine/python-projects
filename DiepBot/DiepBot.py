import pyautogui as ag
import time
import numpy as np
import cv2
import pyscreenshot as ss

'''
import gi.repository
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

def screenshot(x=0, y=0, width=None, height=None):
	window = gtk.gdk.get_default_root_window()
	if not (width and height):
		size = window.get_size()
		if not width:
			width = size[0]
		if not height:
			height = size[1]
	pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
	pixbuf = pixbuf.get_from_drawable(window, window.get_colormap(), x, y, 0, 0, width, height)
	array = pixbuf.get_pixels_array()
	return array
'''

ag.alert(text='', title='', button='Ready')

while True:
	frame = ss.grab();
	#frame.save('frame.png') frame = cv2.imread('frame.png')
	frame = np.array(frame) # convert rgb to bgr
	print(frame)
	hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	cv2.imwrite("hsv.png", hsv)
	squareMask = cv2.inRange(hsv, (40, 50, 90), (60, 70, 110)) # 255, 232, 105
	cv2.imwrite("frame.png", frame)
	cv2.imwrite("mask.png", squareMask)
	#triangleMask = cv2.inRange(frame, (252, 118, 119), (252, 118, 119))
	#pentagonMask = cv2.inRange(frame, (118, 141, 252), (118, 141, 252))
	
	#shapeMask = cv2.bitwise_or(squareMask, triangleMask)
	#shapeMask = cv2.bitwise_or(shapeMask, pentagonMask)
	#target = cv2.bitwise_and(frame, frame, mask=squareMask)
	
	#loc = np.where(target >= 0.1)
	#print(loc)
	
	'''
	yLoc = loc[0]
	xLoc = loc[1]
	
	if xLoc.size > 0 and yLoc.size > 0:
		#print(f'{xLoc[0] + screenWidth / 4} {yLoc[0] + screenHeight / 4}')
		ag.click(xLoc[0] + screenWidth / 4, yLoc[0] + screenHeight / 4)
'''
'''
## Read
img = cv2.imread("sunflower.jpg")

## convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

## mask of green (36,0,0) ~ (70, 255,255)
mask1 = cv2.inRange(hsv, (36, 0, 0), (70, 255,255))

## mask o yellow (15,0,0) ~ (36, 255, 255)
mask2 = cv2.inRange(hsv, (15,0,0), (36, 255, 255))

## final mask and masked
mask = cv2.bitwise_or(mask1, mask2)
target = cv2.bitwise_and(img,img, mask=mask)

cv2.imwrite("target.png", target)
'''
