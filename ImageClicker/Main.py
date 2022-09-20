import pyautogui
import time
import cv2
from PIL import ImageGrab
import numpy
import os
import sys

# in case we run from cmd
os.chdir(os.path.dirname(sys.argv[0]))

# offset uses gpu coordinates, so increasing y lowers click point
def click_target(frame, target, offset = (0, 0), threshold=0.8):
	point = cv2.matchTemplate(frame, target, cv2.TM_CCOEFF_NORMED)
	point = numpy.where(point > threshold)
	if point[0] and point[1]:
		point = point[1][0] + target.shape[1] / 2, point[0][0] + target.shape[0] / 2
		point = (point[0] + offset[0], point[1] + offset[1])
		human_click(point)

def human_click(point):
	pyautogui.moveTo(point[0], point[1], numpy.random.uniform(0, 0.5))
	time.sleep(numpy.random.uniform(0, 0.5))
	pyautogui.mouseDown()
	time.sleep(numpy.random.uniform(0, 0.5))
	pyautogui.mouseUp()
	time.sleep(numpy.random.uniform(0, 0.5))

# pyautogui.alert(title='Image Clicker', text='Ready?', button='OK')

# target = pyautogui.center(pyautogui.locateOnScreen('0.png'))
# pyautogui.click('0.png')
frame = ImageGrab.grab()
frame = numpy.array(frame)
target = cv2.imread('0.png')
click_target(frame, target)
# frame.save('test.png')
