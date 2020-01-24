import pyautogui as ag
import time
import numpy as np
import cv2

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

while True:
	ag.screenshot('screenshot.png')
	im = cv2.imread('screenshot.png', cv2.IMREAD_GRAYSCALE)
	discord = cv2.imread('discord.png', cv2.IMREAD_GRAYSCALE)
	res = cv2.matchTemplate(im, discord, cv2.TM_CCOEFF_NORMED)
	loc = np.where(res >= 0.9)
	print(loc)

#cv2.

#cv2.waitKey(0)
#cv2.destroyAllWindows()
