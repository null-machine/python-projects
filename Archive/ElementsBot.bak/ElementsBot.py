import numpy as np
import cv2
import pyscreenshot as ss
import pyautogui as ag
import time

#ag.alert(text='', title='', button='Ready')

endTurn = cv2.imread('endTurn.png')
defeat = cv2.imread('defeat.png')
discard = cv2.imread('discard.png')

gameDone = cv2.imread('gameDone.png')
bronze = cv2.imread('bronze.png')
startGame = cv2.imread('startGame.png')

def click_target(frame, target, threshold=0.8):
	res = cv2.matchTemplate(frame, target, cv2.TM_CCOEFF_NORMED)
	target = target.shape # switch to dimensions of template
	res = np.where(res > threshold)
	if res[0] and res[1]:
		ag.click(res[1][0] + target[1] / 2, res[0][0] + target[0] / 2)

# def help_click(frame, target)

while True:

	frame = ss.grab();
	frame = np.array(frame)
	'''
	click_target(frame, gameDone)
	click_target(frame, bronze)
	click_target(frame, startGame)
	'''
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
	
	# playing turns
	res = cv2.matchTemplate(frame, endTurn, cv2.TM_CCOEFF_NORMED)
	res = np.where(res >= 0.9)
	if res[0] and res[1]: # len(res) and res.shape are nopes
		startX = res[1][0] + 710
		startY = res[0][0] + 460
		ag.moveTo(startX, startY)
		for i in range(0, 8):
			ag.click(startX, startY - i * 24)
			time.sleep(0.1)
		else:
			ag.press('space')
	
	# treat discard like playing turns
	res = cv2.matchTemplate(frame, discard, cv2.TM_CCOEFF_NORMED) # is shit code
	res = np.where(res >= 0.9)
	if res[0] and res[1]: # len(res) and res.shape are nopes
		ag.moveTo(startX, startY)
		for i in range(0, 8):
			ag.click(startX, startY - i * 24)
		else:
			ag.press('space')
	
	# shitty defeat code
	res = cv2.matchTemplate(frame, defeat, cv2.TM_CCOEFF_NORMED)
	res = np.where(res >= 0.8)
	if res[0] and res[1]:
		ag.click(680, 620) # menu
