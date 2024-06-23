import time
import numpy
import os
from ahk import AHK
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController

ahk = AHK(executable_path="C:/Program Files/AutoHotkey/v1.1.37.01/AutoHotkeyU64.exe")
mouse = MouseController()
keyboard = KeyboardController()

molly_mutex = False
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

# def kill_window():
# 	if (ahk.active_window.process_path != 'C:\Windows\explorer.exe'):
# 		os.system(f'taskkill /f /pid {ahk.active_window.pid}')

def open_logbook():
	ahk.run_script('run \"C:\\Program Files\\VSCodium\\VSCodium.exe\" \"C:\\Home\\Repos\\game-saves\\"')

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
	if not ahk.active_window or ahk.active_window.title != 'Deep Rock Galactic  ':
		return
	ahk.send("{f13 up}")

def lbutton_up_hook():
	if not ahk.active_window or ahk.active_window.title != 'Deep Rock Galactic  ':
		return
	ahk.send('{f13 down}')
	if ahk.key_state('lctrl', mode='P'):
		ahk.send("{' down}")
		frame_sleep()
		ahk.send("{' up}")

def quick_molly():
	global molly_mutex
	if not ahk.active_window or ahk.active_window.title != 'Deep Rock Galactic  ' or molly_mutex:
		return
	key_down = ahk.key_state('q', mode='P')
	molly_mutex = True
	while key_down:
		ahk.send('{rbutton down}')
		frame_sleep()
		ahk.send('{rbutton up}')
		# frame_sleep()
		ahk.send('{. down}')
		frame_sleep()
		ahk.send('{. up}')
		# frame_sleep()
		key_down = ahk.key_state('y', mode='P')
	molly_mutex = False

	# ahk.mouse_move(x=distance, y=-distance, speed=2, relative=True)
	
def rbutton_hook():
	global rbutton_state
	global pickaxe_mutex
	if not ahk.active_window or ahk.active_window.title != 'Deep Rock Galactic  ':
		return
	ahk.send('{f13 up}')
	if pickaxe_mutex:
		return
	pickaxe_mutex = True
	rbutton_state = True
	while rbutton_state:
		ahk.send('{rbutton down}')
		time.sleep(0.6)
		if rbutton_state:
			ahk.send('{rbutton up}')
	pickaxe_mutex = False

def rbutton_up_hook():
	global rbutton_state
	rbutton_state = False
	ahk.send('{f13 down}')

# dice_position = mouse.position
# card_position = mouse.position

# def save_dice_position():
# 	global dice_position
# 	dice_position = mouse.position
# 	mouse.press(Button.right)
# 	frame_sleep()
# 	mouse.release(Button.right)
# 	frame_sleep()
# 	mouse.press(Button.left)
# 	frame_sleep()
# 	mouse.release(Button.left)
# 	frame_sleep()
# 	return

# def save_card_position():
# 	global card_position
# 	card_position = mouse.position
# 	mouse.press(Button.left)
# 	frame_sleep()
# 	mouse.release(Button.left)
# 	frame_sleep()
# 	return

# def retarget_mass():
# 	target_position = mouse.position
# 	mouse.position = dice_position
# 	frame_sleep()
# 	save_dice_position()
# 	mouse.position = card_position
# 	frame_sleep()
# 	save_card_position()
# 	mouse.position = target_position
# 	frame_sleep()
# 	mouse.press(Button.left)
# 	frame_sleep()
# 	mouse.release(Button.left)
# 	frame_sleep()
# 	mouse.move(0, -64)
# 	frame_sleep()
# 	mouse.move(0, 64)
# 	frame_sleep()
# 	return

# system commands
# ahk.add_hotkey('!del', callback=kill_window)
# ahk.add_hotkey('!\'', callback=open_logbook)
ahk.add_hotkey('!`', callback=open_logbook)
ahk.add_hotkey('pause', callback=lambda: ahk.send('{esc}')) # null symbol

# unicode mappings
ahk.add_hotkey('!^space', callback=lambda: ahk.send('{u+202e}')) # rtl override
ahk.add_hotkey('!^+space', callback=lambda: ahk.send('{u+206b}')) # rtl embedding
# ahk.add_hotkey('space', callback=lambda: ahk.send('{u+200a}')) # thin space
# ahk.add_hotkey('space', callback=lambda: ahk.send('{u+2002}')) # thin space
ahk.add_hotkey('!;', callback=lambda: ahk.send('{u+2014}')) # emdash
ahk.add_hotkey('![', callback=lambda: ahk.send('{u+2190}')) # arrow left
ahk.add_hotkey('!]', callback=lambda: ahk.send('{u+2192}')) # arrow right
ahk.add_hotkey('!/', callback=lambda: ahk.send('{u+00f7}')) # division symbol
# ahk.add_hotkey('!0', callback=lambda: ahk.send('{u+00d8}')) # null symbol
ahk.add_hotkey('!s', callback=lambda: ahk.send('{u+00a7}')) # section sign
ahk.add_hotkey('!0', callback=lambda: ahk.send('{u+25ae}')) # cuniform+
# 00bf inverted qmark

# game inputs
ahk.add_hotkey('!o', callback=lambda: keyboard.press(','))
ahk.add_hotkey('ralt & lbutton', callback=lambda: ahk.send('{lbutton down}'))
ahk.add_hotkey('ralt & rbutton', callback=lambda: ahk.send('{rbutton down}'))
ahk.add_hotkey('!wheeldown', callback=click_stack)
ahk.add_hotkey('!wheelup', callback=right_click_stack)
# ahk.add_hotkey('q', callback=emote_zaw)
# ahk.add_hotkey('q up', callback=emote_zaw_cleanup)
ahk.add_hotkey('~*lbutton', callback=lbutton_hook)
ahk.add_hotkey('~*lbutton up', callback=lbutton_up_hook)
ahk.add_hotkey('~*$q', callback=quick_molly)
# ahk.add_hotkey('~*$`', callback=tcf_self)
ahk.add_hotkey('~*$rbutton', callback=rbutton_hook)
ahk.add_hotkey('~*$rbutton up', callback=rbutton_up_hook)
# ahk.add_hotkey('~*q', callback=spiral_flame)

# ahk.add_hotkey('f8 up', callback=save_dice_position)
# ahk.add_hotkey('f7 up', callback=save_card_position)
# ahk.add_hotkey('f6 up', callback=retarget_mass)

# media controls
# ahk.add_hotkey('~mbutton & wheeldown', callback=lambda: ahk.send('{volume_down}'))
# ahk.add_hotkey('~mbutton & wheelup', callback=lambda: ahk.send('{volume_up}'))
# ahk.add_hotkey('~mbutton & lbutton', callback=lambda: ahk.send('{media_play_pause}'))
# ahk.add_hotkey('~mbutton & rbutton', callback=lambda: ahk.send('{media_next}'))
ahk.add_hotkey('ralt & wheeldown', callback=lambda: ahk.send('{volume_down}'))
ahk.add_hotkey('ralt & wheelup', callback=lambda: ahk.send('{volume_up}'))
ahk.add_hotkey('!f2 up', callback=lambda: ahk.send('{media_play_pause}'))
ahk.add_hotkey('!f3 up', callback=lambda: ahk.send('{media_next}'))

# ahk.add_hotkey('ralt & wheeldown', callback=lambda: ahk.send('{volume_down}'))
# ahk.add_hotkey('ralt & wheelup', callback=lambda: ahk.send('{volume_up}'))
# ahk.add_hotkey('ralt & lbutton', callback=lambda: ahk.send('{media_play_pause}'))
# ahk.add_hotkey('ralt & rbutton', callback=lambda: ahk.send('{media_next}'))

ahk.start_hotkeys()
ahk.block_forever()

# embedding: u+202B
# isolate: u+2067
# override: u+202E
# arabic mark: u+061C