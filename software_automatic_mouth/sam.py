from threading import Thread
import subprocess
import os

class Settings:
	pitch = 0
	speed = 0
	mouth = 0
	throat = 0
	save = False
	onFinished = None
	maximum_voices = 2
	def __init__(self, pitch=0, speed=0, mouth=0, throat=0, save=False, onFinished=None, maximum_voices=2):
		self.pitch  = 64-pitch
		self.speed  = 90-speed
		self.mouth  = 140-mouth
		self.throat = 140-throat
		self.save = save
		self.onFinished = onFinished
		self.maximum_voices = maximum_voices

def __processRunning__(process):
	return (process.poll() is None)

__processes__ = []
def __openSamProcess__(args, shell=True, close_fds=True, callback=None):
	global __processes__
	i = len(__processes__)-1
	if len(__processes__) == 0:
		__processes__.append(0)
		i = len(__processes__)-1
	else:
		__processes__[i] = 0
	def run_in_thread(args, shell, close_fds, callback):
		proc = subprocess.Popen(args, shell=shell, close_fds=close_fds)
		__processes__[i] = proc
		proc.wait()
		if proc in __processes__:
			__processes__.remove(proc)
		if callback is not None:
			callback()
		return
	thread = Thread(target=run_in_thread, args=(args, shell, close_fds, callback))
	thread.start()
	return thread

def speak(text, pitch=0, speed=0, mouth=0, throat=0, save=False, onFinished=None, maximum_voices=1):
	global __processes__

	# So the user can pass in a Settings object
	if type(pitch) is Settings:
		speed = pitch.speed
		mouth = pitch.mouth
		throat = pitch.throat
		save = pitch.save
		onFinished = pitch.onFinished
		maximum_voices = pitch.maximum_voices

		pitch = pitch.pitch
	else:
		pitch = 64 - pitch
		speed = 90 - speed
		mouth = 140 - mouth
		throat = 140 - throat

	# If there are more than {maximum_voices} processes (currently broken)
	if len(__processes__) > 0 and len(__processes__) >= maximum_voices-1:
		if __processes__[0] != 0:
			__processes__[0].terminate()
		if len(__processes__) > maximum_voices + 8:
			# So it doesn't somehow overflow with processes and crash your PC
			for process in __processes__:
				if process != 0:
					process.terminate()
			__processes__ = []
	else:
		__openSamProcess__(args=[
			os.path.dirname(os.path.realpath(__file__)) + "/bin/sam.exe",
			"-pitch",  str(pitch),
			"-speed",  str(speed),
			"-mouth",  str(mouth),
			"-throat", str(throat),
			"-wav" if save is not False else "",
			save if save is not False else "",
			text
		], callback=onFinished)
		return len(__processes__) - 1
		
def prompt(text, settings=Settings(), onFinished=None):
	if settings is None and onFinished is not None:
		settings = Settings(onFinished=onFinished)
	speak(text, settings)
	return input(text)
	
def log(text, settings=None, onFinished=None):
	if settings is None and onFinished is not None:
		settings = Settings(onFinished=onFinished)
	print(text)
	return speak(text, settings)

# Not finished
def __speakArray__(array, settings=None):
	can_speak = True
	for i in range(len(array)):
		if can_speak:
			s = None
			if len(array[i]) > 1:
				settings = array[i][1]
			if settings is not None:
				s = speak(array[i][0], settings)
			else:
				s = speak(array[i][0])
			can_speak = False
			if len(__processes__) >= s:
				while __processes__[s] is not None or __processRunning__(__processes__[s]):
					pass
			can_speak = True

speak('testing')