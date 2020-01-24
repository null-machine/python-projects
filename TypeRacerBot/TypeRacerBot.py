import pyautogui as ag
import time
import numpy as np
import cv2
from PIL import Image
import pytesseract
import pyscreenshot as ss


ag.alert(text='', title='', button='Ready')
im = ss.grab(bbox=(130, 510, 880, 740))
im.save('typeText.png')
typeText = pytesseract.image_to_string(Image.open('typeText.png'), lang='eng')


typeText = typeText.replace('|', 'I')
typeText = typeText.replace('\n', ' ')
print(typeText)
ag.typewrite(typeText, interval = 0.01)
