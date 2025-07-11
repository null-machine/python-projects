from tkinter import *
import math
from ahk import AHK, directives
import numpy
import time

ahk = AHK()
ahk.set_coord_mode('Mouse', 'Screen')
directives.MaxHotkeysPerInterval(1)

monitor_shift = 0
root = Tk()
root.attributes('-topmost', True)

bid_prices = []
buy_prices = []
energy_bid = StringVar()
energy_buy = StringVar()

energy_bid.set(44,,,,,,,,,,,,,,00)
energy_buy.set(5000)

humanize = True

rarity_position = (0, 0)
bid_position = (3170, 190)

def frame_sleep():
	if humanize:
		time.sleep(numpy.random.uniform(0.0444, 0.111))
	else:
		time.sleep(0.0444)

def click(point, just_move=False, point_fuzz=4, speed=222, jitter=2, spline_fuzz=0.2):

	def fuzz_point():
		return (numpy.random.uniform(-point_fuzz, point_fuzz + 1), numpy.random.uniform(-point_fuzz, point_fuzz + 1))

	class CursorSpline:

		def __init__(self, start, end, fuzz_range, overextend=0.11):
			delta = numpy.subtract(end, start)
			pivot = numpy.add(end, numpy.multiply(delta, overextend))
			pivot[0] += int(numpy.random.uniform(-fuzz_range, fuzz_range + 1))
			pivot[1] += int(numpy.random.uniform(-fuzz_range, fuzz_range + 1))
			self.pivots = [start, pivot, end]

		def eval(self, time):
			return self.eval_rec(time, 0, len(self.pivots) - 1)
		
		def eval_rec(self, time, startIndex, endIndex):
			if startIndex == endIndex:
				return self.pivots[startIndex]
			start = self.eval_rec(time, startIndex, endIndex - 1)
			end = self.eval_rec(time, startIndex + 1, endIndex)
			delta = numpy.multiply(numpy.subtract(end, start), time)
			return numpy.add(start, delta)

	if humanize:
		position = ahk.get_mouse_position(coord_mode='Screen')
		delta = numpy.subtract(point, position)
		distance = math.sqrt(delta[0] ** 2 + delta[1] ** 2)
		spline = CursorSpline(position, point, distance * spline_fuzz)
		steps = math.ceil(distance / speed) + numpy.random.randint(3)
		for i in range(steps):
			ahk.mouse_position = spline.eval((i + 1) / steps)
		steps = jitter + numpy.random.randint(2)
		for i in range(steps):
			ahk.mouse_position = numpy.add(point, fuzz_point())
		ahk.mouse_position = numpy.add(point, fuzz_point())
	else:
		ahk.mouse_position = numpy.add(point, fuzz_point())
	frame_sleep()
	if not just_move:
		ahk.key_down('lbutton')
		time.sleep(numpy.random.uniform(0.0444, 0.111))
		ahk.key_up('lbutton')
		time.sleep(numpy.random.uniform(0.0444, 0.111))


def rbutton_hook():
	global rarity_position
	rarity_position = ahk.get_mouse_position(coord_mode='Screen')
	print(f'rarity position: {rarity_position}')

# def rbutton_up_hook():
# 	global bid_position
# 	bid_position = ahk.get_mouse_position(coord_mode='Screen')
# 	print(f'bid position: {bid_position}')

ahk.add_hotkey('$~*rbutton', callback=rbutton_hook)
# ahk.add_hotkey('$~*rbutton up', callback=rbutton_up_hook)

def update():
	try:
		bid = float(energy_bid.get())
		buy = float(energy_buy.get())
	except:
		return
	for i in range(len(bid_prices)):
		if i == 0:
			bid_prices[i].set(math.ceil(bid / 6 / 0.9))
			buy_prices[i].set(math.ceil(buy / 6 / 0.9))
		elif i == 1:
			bid_prices[i].set(math.ceil(bid * 2 / 3 / 0.9))
			buy_prices[i].set(math.ceil(buy * 2 / 3 / 0.9))
		elif i == 2:
			bid_prices[i].set(math.ceil(bid * 4 / 3 / 0.9))
			buy_prices[i].set(math.ceil(buy * 4 / 3 / 0.9))
		elif i == 3:
			bid_prices[i].set(math.ceil(bid / 5 / 0.9))
			buy_prices[i].set(math.ceil(buy / 5 / 0.9))

energy_bid.trace('w', lambda name, index, mode: update())
energy_buy.trace('w', lambda name, index, mode: update())

def post_auction(i):
	global rarity_position
	global bid_position
	cursor_position = ahk.get_mouse_position(coord_mode='Screen')
	click(bid_position)
	click(rarity_position)
	click(bid_position)
	print(f'{i}')
	ahk.send(f'{{ctrl down}}a{{ctrl up}}{bid_prices[i].get()}{{tab}}{{ctrl down}}a{{ctrl up}}{buy_prices[i].get()}')
	click(cursor_position, True)

def create_post_auction(i):
	return lambda: post_auction(i)

Label(root, text='Energy').grid(row=0, column=0, sticky='w', padx=16, pady=8)
Entry(root, textvariable=energy_bid).grid(row=0, column=1, padx=16, pady=8)
Entry(root, textvariable=energy_buy).grid(row=0, column=2, padx=16, pady=8)

for i in range(1, 5):
	if i == 1:
		text = 'Simple'
	elif i == 2:
		text = 'Advanced'
	elif i == 3:
		text = 'Elite'
	elif i == 4:
		text = 'Spark'
	bid_price = IntVar()
	bid_prices.append(bid_price)
	buy_price = IntVar()
	buy_prices.append(buy_price)
	Button(root, text=text, command=create_post_auction(i - 1)).grid(row=i, column=0, sticky='w', padx=16, pady=8)
	Label(root, textvariable=bid_price, width=8).grid(row=i, column=1, sticky='w', padx=16, pady=8)
	Label(root, textvariable=buy_price, width=8).grid(row=i, column=2, sticky='w', padx=16, pady=8)

update()

ahk.start_hotkeys()

root.mainloop()