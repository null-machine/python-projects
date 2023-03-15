import pyautogui as ag
import time

ag.PAUSE = 0

while True:
	state = ag.pixel(943, 801)
	#catch = ag.pixel(1249, 716)
	print(state)
	if state == (165, 211, 56): # casting
		print('casting')
		time.sleep(1)
		ag.press('space') 
		time.sleep(0.763) # 0.702 for normal
		ag.press('space')
		print('cast finished')
	#elif catch == (77, 254, 0): # catching 
		#or catch == (254, 202, 0)
	#	print('catching')
	#	ag.press('space')
	#elif state == (151, 183, 51) or state == (109, 142, 9) or state == (39, 52, 7): # trading or fail
	#	ag.press('space')
	#	time.sleep(1)
