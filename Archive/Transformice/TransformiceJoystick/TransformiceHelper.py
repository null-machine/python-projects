from pynput import mouse
from pynput.keyboard import Key, Controller
import time

time.sleep(2)

pivotX = 1049
pivotY = 714
keyboard = Controller()

def on_move(x, y):
	#print('Pointer moved to {0}'.format((x, y)))
	if x < pivotX:
		print('left')
		keyboard.release(Key.right)
		keyboard.press(Key.left)
		#ag.keyUp('right')
		#ag.keyDown('left')
	else:
		print('right')
		keyboard.release(Key.left)
		keyboard.press(Key.right)
		#ag.keyUp('left')
		#ag.keyDown('right')
	if y < pivotY:
		print('up')
		keyboard.press(Key.up)
		#ag.keyDown('up')
	else:
		print('down')
		keyboard.release(Key.up)
		#ag.keyUp('up')

def on_click(x, y, button, pressed):
	print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))

def on_scroll(x, y, dx, dy):
	print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
	listener.join()

#while(active):
#	print('cursor position: {0}'.format(mouse.position))
