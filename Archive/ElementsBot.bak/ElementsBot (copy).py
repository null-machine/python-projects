import numpy as np
import cv2
import pyscreenshot as ss
import pyautogui as ag
import time

#ag.alert(text='', title='', button='Ready')

endTurn = cv2.imread('endTurn.png')
gameDone = cv2.imread('gameDone.png')
defeat = cv2.imread('defeat.png')

while True:

	frame = ss.grab();
	frame = np.array(frame)
	
	# playing turns
	res = cv2.matchTemplate(frame, endTurn, cv2.TM_CCOEFF_NORMED)
	res = np.where(res >= 0.9)
	if res[0].size > 0 and res[1].size > 0: # len(res) and res.shape are nopes
		startX = res[1][0] + 710
		startY = res[0][0] + 460
		ag.moveTo(startX, startY)
		for i in range(0, 8):
			ag.click(startX, startY - i * 24)
		else:
			ag.press('space')
	
	# collecting rewards and resetting
	res = cv2.matchTemplate(frame, gameDone, cv2.TM_CCOEFF_NORMED)
	res = np.where(res >= 0.8)
	if res[0].size > 0 and res[1].size > 0:
		startX = res[1][0]
		startY = res[0][0]
		ag.click(startX + 125, startY - 125) # spin
		time.sleep(8)
		ag.click(startX - 340, startY - 470) # menu
		time.sleep(2)
		ag.click(startX - 233, startY - 305) # bronze
		time.sleep(2)
		ag.click(startX - 176, startY - 63) # start

'''

	try:
		endTurn = ag.locateOnScreen('endTurn.png', confidence=0.8) # region=(0, 0, screenWidth / 2, screenHeight / 2), 
		ag.moveTo(endTurn.x + 710, endTurn.y + 450)
		for i in range(0, 8): # click cards from bottom up
			ag.click()
			ag.moveRel(0, -24)
		else:
			ag.press('space') # end turn after cards played
	except:
		print('not my turn')
		try:
			ag.locateOnScreen('spinAll.png', confidence=0.8,)
			print('clicking spin all')
			ag.click(750, 640) # spin all
			time.sleep(8)
			ag.click(290, 300) # menu
			time.sleep(2)
			ag.click(390, 465) # bronze
			time.sleep(2)
			ag.click(450, 705) # start game
		except:
			try:
				ag.locateOnScreen('defeat.png', confidence=0.8,)
				print('defeated')
				ag.click(680, 620) # menu
				time.sleep(2)
				ag.click(390, 465) # bronze
				time.sleep(2)
				ag.click(450, 705) # start game
			except:
				print('game still going')
		time.sleep(1)
'''
