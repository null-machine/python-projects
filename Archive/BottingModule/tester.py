import botting as b

discord = b.cv2.imread('screenshot_1.png')

print('hi')

while True:
	print('hello')
	frame = b.parse_screen()
	b.quick_click(frame, discord, threshold=0.5)
