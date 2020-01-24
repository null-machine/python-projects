from pynput import keyboard, mouse
import pyautogui as ag

controller = keyboard.Controller()

def keybind(key):
	return {
		keyboard.Key.home : '1v',
		keyboard.Key.end : '8c ',
		keyboard.Key.page_up : '3',
		keyboard.Key.page_down : '9c ',
		keyboard.Key.insert : 'n',
		keyboard.Key.delete : 'j',
		keyboard.KeyCode.from_char('/') : '7 ',
		keyboard.KeyCode.from_char('*') : '4 ',
		keyboard.KeyCode.from_char('-') : '5 ',
		keyboard.KeyCode.from_char('+') : '2',
		keyboard.KeyCode.from_vk(65437) : 'e',
		
		mouse.Button.right : 'c',
		mouse.Button.middle : ' ',
		mouse.Button.button9 : 'v'
	}.get(key, '')


def on_press(key):
	bind = keybind(key)
	if bind == 'n':
		ag.keyDown('ctrl')
	elif bind != '':
		ag.keyUp('ctrl')
		controller.type(bind)
		#ag.typewrite(bind)
	

def on_click(x, y, button, pressed):
	if pressed:
		bind = keybind(button)
		if bind != '':
			controller.type(bind)

with keyboard.Listener(on_press=on_press) as listener:
	with mouse.Listener(on_click=on_click) as listener:
		listener.join()
