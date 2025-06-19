from ahk import AHK
import dxcam 
import cv2
import time
import math
import numpy
import os
import sys
import _thread

ahk = AHK()
camera = dxcam.create(output_idx=0)
monitor_shift = 0
humanize = True

halting = False

class Target:

	def __init__(self, name, image, action, offset):
		self.name = name
		self.image = image
		self.action = action
		self.offset = offset

def print_update(text):
	sys.stdout.write('\033[K')
	print(text, end='\r')
	# print(f'\r{text}', end='')
	# print(text)

def frame_sleep():
	if humanize:
		time.sleep(numpy.random.uniform(0.0444, 0.111))
	else:
		time.sleep(0.0444)

def click(point, point_fuzz=4, speed=333, jitter=2, spline_fuzz=0.2):

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
	ahk.key_down('lbutton')
	frame_sleep()
	ahk.key_up('lbutton')
	frame_sleep()

def match_template(frame, target, threshold=0.035):
	result = cv2.matchTemplate(frame, target, cv2.TM_SQDIFF_NORMED)
	min_value, max_value, min_point, max_point = cv2.minMaxLoc(result)
	# cv2.imshow("target", target)
	# cv2.imshow("frame", frame)
	# cv2.waitKey(0)
	if min_value < threshold:
		point = monitor_shift + min_point[0] + target.shape[1] / 2, min_point[1] + target.shape[0] / 2
		return point
	else:
		return None

def template_match_loop():
	if sys.argv[0] != 'main.py':
		os.chdir(os.path.dirname(sys.argv[0]))
	files = [file for file in os.listdir() if file.endswith('.png')]
	print(files)
	targets = {file : Target(file, cv2.imread(file), click, (0, 0)) for file in files}
	# targets['3.png'].offset = (0, 50)
	# targets['0win.png'].action = win_action
	frame = camera.grab()
	while not halting:
		for target in targets.values():
			print_update(f'{target.name}')
			capture = camera.grab()
			if capture is not None: # screen has been updated
				frame = capture
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			point = match_template(frame, target.image)
			if point is not None and target.action:
				print(f'{target.name}: {target.action.__name__}')
				target.action(numpy.add(point, target.offset))
		# print_update('sleeping')
		# time.sleep(2)
		

def kill():
	global halting
	halting = True
	# _thread.interrupt_main()
	print('--- halt semaphore set ---')

ahk.add_hotkey('ralt & lalt', callback=kill)
ahk.start_hotkeys()

template_match_loop()

# ahk.block_forever()
