import botting as b
import time
from multiprocessing import Process
import pyautogui as ag
import pyscreenshot as ss

ag.PAUSE = 0

def cast():
	while True:
		ag.alert(text='', title='', button='Cast')
		time.sleep(0.763)
		ag.press('space')
		time.sleep(0.763) # 0.702 for normal
		ag.press('space')

cast()

#b.multiprocess(cast, catch)

	#elif catch == (77, 254, 0): # catching 
		#or catch == (254, 202, 0)
	#	print('catching')
	#	ag.press('space')
	#elif state == (151, 183, 51) or state == (109, 142, 9) or state == (39, 52, 7): # trading or fail
	#	ag.press('space')
	#	time.sleep(1)

