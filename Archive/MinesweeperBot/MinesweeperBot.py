import pyautogui as ag
import time
import numpy as np
import cv2
import pyscreenshot as ss

screenWidth, screenHeight = ag.size()

ag.alert(text='', title='', button='Ready')

while True:
	frame = ss.grab();
	frame.save('frame.png')
	#ag.screenshot('screenshot.png', region=(screenCenter[0], screenCenter[1], screenCenter[2], screenCenter[3])) #region=(*screenCenter)
	frame = cv2.imread('frame.png', cv2.IMREAD_COLOR)
	timer = cv2.imread('hidden.png', cv2.IMREAD_COLOR)
	res = cv2.matchTemplate(frame, timer, cv2.TM_CCOEFF_NORMED)
	loc = np.where(res >= 0.9999)
	print(loc)
	xLoc = loc[0]
	yLoc = loc[1]
	
	if xLoc.size > 0 and yLoc.size > 0:
		ag.click(xLoc[0] + 8, yLoc[0] + 8)
	
	'''
	if xLoc.size == 1 && yLoc.size == 1: 
		gridEndX = xLoc[0] + 249
		gridStartX = gridEndX + 480
		gridEndY = yLoc[0] + 289
		gridStartY = gridEndY + 256
	'''
		
	
	#print

#cv2.

#cv2.waitKey(0)
#cv2.destroyAllWindows()
