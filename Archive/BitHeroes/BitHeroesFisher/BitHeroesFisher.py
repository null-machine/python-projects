import botting as b
import time
from multiprocessing import Process
import pyautogui as ag
import pyscreenshot as ss

ag.PAUSE = 0


def catch():
	while True: # 1249, 716
		frame = b.parse_screen((1249, 725, 1250, 726))
		target = b.search_pixel(frame, (77, 254, 0))
		print(target)
		if target is not None:
			ag.press('space')

catch()
