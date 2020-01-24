import pyautogui as ag
import time
import numpy as np
import cv2
from PIL import Image
import pytesseract
import pyscreenshot as ss


ag.alert(text='', title='', button='Ready')



while True:
	#im = ss.grab(bbox=(510, 270, 840, 720))
	#im.save('typeText.png')
	typeText = pytesseract.image_to_string(Image.open('stop.jpeg'), lang='eng')
	#typeText = typeText.replace('\n', '')
	print(typeText)
	#ag.typewrite(typeText, interval=0.01)
