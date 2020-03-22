import pyautogui as bot
import time

# colors for 1130, 675
# (17, 66, 85) mission opened
# (171, 125, 61) axe loaded
# (19, 23, 31) lobby loaded
# (154, 176, 206) advance loaded
# (87, 199, 95) corner wall hit

# colors for 1300, 660
# (13, 52, 66) mission opened, dead
# (17, 66, 85)
# (171, 125, 61) axe loaded
# (19, 23, 31) lobby loaded
# (154, 176, 206) advance loaded
# (87, 199, 95) corner wall hit

# coords
# (1315, 560) mission start
# (1020, 680) advance now


def update_state():
	global state
	state = bot.pixel(1130, 675)

def color_wait(r, g, b):
	update_state()
	while (state != (r, g, b)):
		time.sleep(1)
		update_state()

# while True:
# 	print(bot.pixel(1300, 660))

time.sleep(2)
while True:
	# walk to elevator
	bot.keyDown('n')
	bot.keyDown('t')
	time.sleep(0.4)
	bot.keyUp('n')
	time.sleep(0.6)
	bot.keyDown('r')
	bot.keyUp('t')
	time.sleep(0.2)
	bot.press('-')
	time.sleep(1)
	bot.keyDown('s')

	# click advance now
	color_wait(154, 176, 206)

	bot.keyUp('s')
	bot.keyUp('r')
	time.sleep(1)
	bot.click(1020, 680, button='right')
	color_wait(171, 125, 61)

	# walk to boxes
	bot.keyDown('n')
	bot.press('-')
	time.sleep(1)
	bot.keyDown('t')
	time.sleep(8)
	bot.press('-')

	# loot time
	color_wait(87, 199, 95)
	bot.keyUp('n')
	bot.keyUp('t')
	bot.press('l')
	bot.keyDown('s')
	time.sleep(0.23)
	bot.keyUp('s')
	bot.click(button='right')
	time.sleep(0.7)
	bot.click(button='right')
	bot.keyDown('n')
	time.sleep(2.2)
	bot.keyUp('n')

	# reset
	bot.press('m')
	color_wait(17, 66, 85)
	bot.click(1315, 560, button='right')
	bot.move(-600, 0)
	color_wait(19, 23, 31)
