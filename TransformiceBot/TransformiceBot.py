import numpy as np
import cv2
import pyautogui as ag
import time
import pyscreenshot as ss


while True:
	frame = ss.grab(bbox=(500, 300, 1300, 670)); # 560, 300, 800, 370
	frame.save('frame.png')
	frame = cv2.imread('frame.png', cv2.IMREAD_COLOR)
	target = cv2.imread('playerIdle.png', cv2.IMREAD_COLOR)
	res = cv2.matchTemplate(frame, target, cv2.TM_CCOEFF_NORMED)
	loc = np.where(res >= 0.9)
	print(loc)
	yLoc = loc[0] + 300
	xLoc = loc[1] + 500
	
	if xLoc.size > 0 and yLoc.size > 0:
		ag.click(xLoc[0], yLoc[0])
