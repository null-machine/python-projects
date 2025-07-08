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

class Human:

	def __init__(self):
		self.ahk = AHK()
		self.ahk.set_coord_mode('Mouse', 'Screen')
