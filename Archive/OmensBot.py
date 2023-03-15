import pyautogui as ag
import time

while True:
	state = ag.pixel(461, 871)
	print(state)
	if state == (33, 28, 24): # our turn
		for i in range(0, 4): # play hand
			ag.click(505, 791)
		for i in range(0, 4): # buy cards
			ag.click(40, 500 + i * 110)
		ag.press('space')
		time.sleep(2)
	elif state == (5, 4, 4): # game end
		ag.click(1093, 874)
	elif state == (0, 0, 0): # click to continue
		ag.click(1093, 874)
	elif state == (2, 1, 1): # level up
		ag.click(956, 860)
