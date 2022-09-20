import pyautogui
import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

pyautogui.alert(title='Image Clicker', text='Ready?', button='OK')

# target = pyautogui.center(pyautogui.locateOnScreen('0.png'))
pyautogui.click('0.png')
