import time
import numpy
import os
from ahk import AHK, directives
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController

import ctypes

target_window = None

CF_TEXT = 1

kernel32 = ctypes.windll.kernel32
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32 = ctypes.windll.user32
user32.GetClipboardData.restype = ctypes.c_void_p

def get_clipboard_text():
	user32.OpenClipboard(0)
	try:
		if user32.IsClipboardFormatAvailable(CF_TEXT):
			data = user32.GetClipboardData(CF_TEXT)
			data_locked = kernel32.GlobalLock(data)
			text = ctypes.c_char_p(data_locked)
			value = text.value
			kernel32.GlobalUnlock(data_locked)
			return str(value)[2:-1]
	finally:
		user32.CloseClipboard()

ahk = AHK(executable_path="C:/Program Files/AutoHotkey/v1.1.37.01/AutoHotkeyU64.exe")
# directives.MaxHotkeysPerInterval(10)
mouse = MouseController()
keyboard = KeyboardController()

molly_mutex = False
zipline_mutex = False
pickaxe_mutex = False
rbutton_state = False

def frame_sleep():
	time.sleep(numpy.random.uniform(0.04, 0.09))

def small_sleep():
	time.sleep(numpy.random.uniform(0.16, 0.25))

def long_sleep():
	time.sleep(numpy.random.uniform(0.49, 0.64))

def click_point(point):
	mouse.position = point
	mouse.move(numpy.random.uniform(-4, 4), numpy.random.uniform(-4, 4))
	mouse.press(Button.left)
	frame_sleep()
	mouse.release(Button.left)
	small_sleep()

def check_window(title):
	return ahk.active_window and ahk.active_window.title is not None and ahk.active_window.title.startswith(title)

# def kill_window():
# 	if (ahk.active_window.process_path != 'C:\Windows\explorer.exe'):
# 		os.system(f'taskkill /f /pid {ahk.active_window.pid}')

def open_logbook():
	ahk.run_script('run \"C:\\Program Files\\VSCodium\\VSCodium.exe\" \"C:\\Home\\Repos\\library\\"')

def click_stack():
	for i in range(32):
		mouse.press(Button.left)
		mouse.release(Button.left)

def right_click_stack():
	for i in range(32):
		mouse.press(Button.right)
		mouse.release(Button.right)
		
# def emote_zaw():
# 	if (ahk.active_window.title != 'Warframe'):
# 		ahk.send('{q down}')
# 		return
# 	forward_down = ahk.key_state(',', mode='P')
# 	ahk.send('{, up}')
# 	ahk.send('{rbutton down}')
# 	ahk.send('{wheelup}')
# 	frame_sleep()
# 	ahk.send('{wheelup}')
# 	frame_sleep()
# 	ahk.send('\'')
# 	small_sleep()
# 	ahk.send('{rbutton up}')
# 	ahk.send('j')
# 	frame_sleep()
# 	ahk.send('{lshift down}')
# 	frame_sleep()
# 	ahk.send('{lshift up}')
# 	if forward_down:
# 		ahk.send('{, down}')

# def emote_zaw_cleanup():
# 	if (ahk.active_window.title != 'Warframe'):
# 		ahk.send('{q up}')
# 		return

def lbutton_hook():
	if not check_window('Deep Rock Galactic'):
		return
	ahk.send("{scrolllock up}")

def lbutton_up_hook():
	if not check_window('Deep Rock Galactic'):
		return
	ahk.send('{scrolllock down}')
	if ahk.key_state('lctrl', mode='P'):
		ahk.send("{' down}")
		frame_sleep()
		ahk.send("{' up}")

def quick_molly():
	global molly_mutex
	if not check_window('Deep Rock Galactic') or molly_mutex:
		return
	key_down = ahk.key_state('q', mode='P')
	molly_mutex = True
	while key_down:
		ahk.send('{rbutton down}')
		frame_sleep()
		ahk.send('{rbutton up}')
		ahk.send('{. down}')
		frame_sleep()
		ahk.send('{. up}')
		key_down = ahk.key_state('q', mode='P')
	molly_mutex = False

def quick_zipline():
	global zipline_mutex
	if not check_window('Deep Rock Galactic') or zipline_mutex:
		return
	key_down = ahk.key_state('y', mode='P')
	zipline_mutex = True
	while key_down:
		ahk.send('{space down}')
		small_sleep()
		ahk.send('{space up}')
		ahk.send('{. down}')
		frame_sleep()
		ahk.send('{. up}')
		key_down = ahk.key_state('y', mode='P')
	zipline_mutex = False

# def drg_sprint():
# 	if not check_window('Deep Rock Galactic') or zipline_mutex:
# 		return
# 	ahk.send('{scrolllock down}')

	# ahk.mouse_move(x=distance, y=-distance, speed=2, relative=True)
	
def rbutton_hook():
	global rbutton_state
	global pickaxe_mutex
	rbutton_state = True
	if not check_window('Deep Rock Galactic'):
		return
	ahk.send('{scrolllock up}')
	# if pickaxe_mutex:
	# 	return
	# pickaxe_mutex = True
	# while rbutton_state:
	# 	ahk.send('{rbutton down}')
	# 	time.sleep(0.6)
	# 	if rbutton_state:
	# 		ahk.send('{rbutton up}')
	# pickaxe_mutex = False

def rbutton_up_hook():
	global rbutton_state
	rbutton_state = False
	if not check_window('Deep Rock Galactic'):
		return
	ahk.send('{scrolllock down}')

dice_position = mouse.position
card_position = mouse.position

def save_dice_position():
	global dice_position
	if not check_window('LibraryOfRuina'):
		return
	dice_position = mouse.position
	frame_sleep()
	mouse.press(Button.right)
	frame_sleep()
	mouse.release(Button.right)
	frame_sleep()
	mouse.press(Button.left)
	frame_sleep()
	mouse.release(Button.left)
	frame_sleep()
	return

def save_card_position():
	global card_position
	if not check_window('LibraryOfRuina'):
		return
	card_position = mouse.position
	frame_sleep()
	mouse.press(Button.left)
	frame_sleep()
	mouse.release(Button.left)
	frame_sleep()
	return

def retarget_mass():
	if not check_window('LibraryOfRuina'):
		return
	target_position = mouse.position
	mouse.position = dice_position
	frame_sleep()
	save_dice_position()
	mouse.position = card_position
	frame_sleep()
	save_card_position()
	mouse.position = target_position
	frame_sleep()
	mouse.press(Button.left)
	frame_sleep()
	mouse.release(Button.left)
	frame_sleep()
	mouse.move(0, -64)
	frame_sleep()
	mouse.move(0, 64)
	frame_sleep()
	return

def quick_on_play():
	if not check_window('LibraryOfRuina'):
		return
	target_position = mouse.position
	mouse.press(Button.left)
	frame_sleep()
	mouse.release(Button.left)
	frame_sleep()
	mouse.position = dice_position
	frame_sleep()
	mouse.press(Button.left)
	frame_sleep()
	mouse.release(Button.left)
	frame_sleep()
	mouse.position = target_position
	frame_sleep()
	return

watching_pixel = False

def toggle_pixel_watch():
	global watching_pixel
	if watching_pixel:
		stop_pixel_watch()
	else:
		start_pixel_watch()

def start_pixel_watch():
	global watching_pixel
	watching_pixel = True
	while (watching_pixel):
		# if ahk.pixel_get_color(960, 600) == '0xF99CFF':
		if ahk.pixel_get_color(978, 605) == '0xAF62BD':
			mouse.press(Button.left)
			frame_sleep()
			time.sleep(0.1)
			mouse.release(Button.left)
			small_sleep()


def stop_pixel_watch():
	global watching_pixel
	watching_pixel = False

def ytdlp():
	ahk.run_script(f'run \"C:\\Home\\yt-dlp\\yt-dlp.exe" {get_clipboard_text()}')


def better_fullscreen():
	print('fullscreen attempt')
	window = ahk.win_get('a')
	window.set_style('^0xC00000')
	window.maximize()
	# xywh = window.get_position()
	# window.move(1980 / 2 - xywh[2] / 2, 1080 / 2 - xywh[3] / 2)
	# window.move(xywh[0], 0)
# def wheel_pgup():
# 	if not check_window('Terraria'):
# 		return
# 	ahk.send('{pgup down}')
# 	# frame_sleep()
# 	ahk.send('{pgup up}')
# 	return

# def wheel_pgdn():
# 	if not check_window('Terraria'):
# 		return
# 	ahk.send('{pgdn down}')
# 	# frame_sleep()
# 	ahk.send('{pgdn up}')
# 	return

# system commands
# ahk.add_hotkey('!del', callback=kill_window)
# ahk.add_hotkey('!\'', callback=open_logbook)
ahk.add_hotkey('$!`', callback=open_logbook)
ahk.add_hotkey('$!insert', callback=ytdlp)
ahk.add_hotkey('$pause', callback=lambda: ahk.send('{esc}'))

ahk.add_hotkey('ralt & f11', callback=better_fullscreen)

# unicode mappings
ahk.add_hotkey('$!^space', callback=lambda: ahk.send('{u+202e}')) # rtl override
ahk.add_hotkey('$!^+space', callback=lambda: ahk.send('{u+206b}')) # rtl embedding
# ahk.add_hotkey('space', callback=lambda: ahk.send('{u+200a}')) # thin space
# ahk.add_hotkey('space', callback=lambda: ahk.send('{u+2002}')) # thin space
# ahk.add_hotkey('!;', callback=lambda: ahk.send('{u+2014}')) # emdash
ahk.add_hotkey('$![', callback=lambda: ahk.send('{u+2190}')) # arrow left
ahk.add_hotkey('$!]', callback=lambda: ahk.send('{u+2192}')) # arrow right
ahk.add_hotkey('$!/', callback=lambda: ahk.send('{u+00f7}')) # division symbol
# ahk.add_hotkey('!0', callback=lambda: ahk.send('{u+00d8}')) # null symbol
ahk.add_hotkey('$!s', callback=lambda: ahk.send('{u+00a7}')) # section sign

# game inputs
ahk.add_hotkey('rctrl & lbutton', callback=lambda: ahk.send('{lbutton down}'))
ahk.add_hotkey('rctrl & rbutton', callback=lambda: ahk.send('{rbutton down}'))
# ahk.add_hotkey('$!wheeldown', callback=click_stack)
# ahk.add_hotkey('$!wheelup', callback=right_click_stack)

ahk.add_hotkey('$scrolllock', callback=toggle_pixel_watch)
# ahk.add_hotkey('q', callback=emote_zaw)
# ahk.add_hotkey('q up', callback=emote_zaw_cleanup)

# ahk.add_hotkey('$wheelup', callback=wheel_pgup)
# ahk.add_hotkey('$wheeldown', callback=wheel_pgdn)

# ahk.add_hotkey('$~*lbutton', callback=lbutton_hook)
# ahk.add_hotkey('$~*lbutton up', callback=lbutton_up_hook)
# ahk.add_hotkey('$~*q', callback=quick_molly)
# ahk.add_hotkey('$~*y', callback=quick_zipline)
# ahk.add_hotkey('$~*rbutton', callback=rbutton_hook)
# ahk.add_hotkey('$~*rbutton up', callback=rbutton_up_hook)

# ahk.add_hotkey('~*,', callback=drg_sprint)



# ahk.add_hotkey('$~*backspace', callback=lalt_hook)

# ahk.add_hotkey('f8 up', callback=save_dice_position)
# ahk.add_hotkey('f7 up', callback=save_card_position)
# ahk.add_hotkey('f6 up', callback=retarget_mass)
# ahk.add_hotkey('f5 up', callback=quick_on_play)

# media controls
# ahk.add_hotkey('~mbutton & wheeldown', callback=lambda: ahk.send('{volume_down}'))
# ahk.add_hotkey('~mbutton & wheelup', callback=lambda: ahk.send('{volume_up}'))
# ahk.add_hotkey('~mbutton & lbutton', callback=lambda: ahk.send('{media_play_pause}'))
# ahk.add_hotkey('~mbutton & rbutton', callback=lambda: ahk.send('{media_next}'))
ahk.add_hotkey('$!;', callback=lambda: ahk.send('{u+2014}'))
# ahk.add_hotkey('$!q', callback=lambda: ahk.send('{volume_up}'))
# ahk.add_hotkey('$!f2 up', callback=lambda: ahk.send('{media_play_pause}'))
# ahk.add_hotkey('$!f3 up', callback=lambda: ahk.send('{media_next}'))

# ahk.add_hotkey('ralt & wheeldown', callback=lambda: ahk.send('{volume_down}'))
# ahk.add_hotkey('ralt & wheelup', callback=lambda: ahk.send('{volume_up}'))
# ahk.add_hotkey('ralt & lbutton', callback=lambda: ahk.send('{media_play_pause}'))
# ahk.add_hotkey('ralt & rbutton', callback=lambda: ahk.send('{media_next}'))

ahk.add_hotkey('ralt & left', callback=lambda: mouse.move(-1, 0))
ahk.add_hotkey('ralt & right', callback=lambda: mouse.move(1, 0))
ahk.add_hotkey('ralt & up', callback=lambda: mouse.move(0, -1))
ahk.add_hotkey('ralt & down', callback=lambda: mouse.move(0, 1))

# ahk.add_hotkey('appskey', callback=lambda: alt_esc())

# def alt_esc():
# 	ahk.send('{alt down}')
# 	ahk.send('{esc}')
# 	ahk.send('{alt up}')

# def update_window():
# 	global target_window
# 	target_window = ahk.win_get('a')
# 	print(f'target window: {target_window}')

# def send_pgup():
# 	global target_window
# 	# ahk.control_send(control=target_window, keys='pgup')
# 	ahk.control_send(title='global.py - python-projects - VSCodium', keys='wheelup', detect_hidden_windows=True)
# 	print("what")
# 	# ahk.control_send('Edit1', 'pgup', target_window)
	

# ahk.add_hotkey('!f5', callback=lambda: update_window())
# ahk.add_hotkey('!pgup', callback=lambda: send_pgup())

def matsune():
	last_window = ahk.win_get_title('A')
	speech_input = ahk.input_box(height=99)
	if speech_input:
		speech_input = speech_input.replace(' ', '-')
	ahk.win_activate('ahk_exe CeVIO AI.exe')
	if 'CeVIO AI' in ahk.win_get_title('A'):
		ahk.send('{f2}')
		ahk.send_input(speech_input)
		ahk.send('{enter}')
		ahk.win_activate(last_window)

ahk.add_hotkey('!enter', callback=lambda: matsune())

ahk.start_hotkeys()
ahk.block_forever()

# embedding: u+202B
# isolate: u+2067
# override: u+202E
# arabic mark: u+061C
