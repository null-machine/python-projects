# import pyautogui as ag
from PIL import Image
import pytesseract
import keyboard
# import pyscreenshot as ss

# ag.alert(text='', title='', button='Ready')
# im = ss.grab(bbox=(130, 510, 880, 740))
# im.save('typeText.png')
typeText = pytesseract.image_to_string(Image.open('typeText.png'), lang='eng')
typeText = typeText.replace('|', 'I')
typeText = typeText.replace('\n', ' ')
print(typeText)
keyboard.write(typeText)
