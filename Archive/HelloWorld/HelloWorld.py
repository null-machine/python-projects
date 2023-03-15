import numpy as np
#import pyscreenshot as ImageGrab
import cv2
import pyautogui as ag
import time

'''
# draw square spiral
time.sleep(5)
distance = 100
while distance > 0:
	ag.dragRel(distance, 0)
	distance -= 5
	ag.dragRel(0, distance)
	ag.dragRel(-distance, 0)
	distance -= 5
	ag.dragRel(0, -distance)


'''
#parse image
while(True):
	#frame = np.array(ImageGrab.grab(bbox = (200, 200, 800, 640)))
	frame = np.array(ag.screenshot(region=(0,0, 300, 400)))
	#printscreen_numpy = np.array(printscreen_pil.getdata(),dtype='uint8')\
	#.reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 
	cv2.imshow('Vision', cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB))
	if cv2.waitKey(20) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
