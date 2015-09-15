import speech_recognition as sr
import time, pyttsx, threading, sys, os, signal, thread, subprocess
from sys import platform as _platform

class JarvisIO():
	def __init__(self):
		self.r = sr.Recognizer()
		self.r.dynamic_energy_threshold = False
		self.r.energy_threshold = 500
		self.t = []
		self.engine = pyttsx.init()
		# self.engine.setProperty('rate', 10)
		self.talker = None
		os.setpgrp()
		pass

	def listen_for(self, keyword, blocking=True):
		keyword = keyword.lower()
		def callback(recognizer, audio): 
		    try:
		        # print("You said " + recognizer.recognize(audio)) 
		        text = recognizer.recognize(audio)
		        if keyword in text.lower().split():
		        	print("I heard the keyword: " + keyword)
		        	thread.exit()
		    except LookupError:
		        pass # didn't hear what we were looking for
		    except IndexError:
		    	print("No internet connection")
		    except KeyError:
		    	print("API Key Error")
		temp = self.r.listen_in_background(sr.Microphone(), callback)
		self.t.append(temp)
		if blocking:
			temp.join()
			self.t.remove(temp)

	def next(self):
		with sr.Microphone() as source:
		    audio = self.r.listen(source)  

		try:
			text = self.r.recognize(audio)
			print("You said: '" + text + "'") 
		except LookupError:
			text = ""
			print("Could not understand audio")
		return text.lower()

	def say(self, text, timeout=5):
		for p in '"-!\'':
			text = text.replace(p, '')
		if _platform == "linux" or _platform == "linux2": # linux
		    pass
		elif _platform == "darwin": # OS X
			subprocess.call(['say', text])
			pass
		elif _platform == "win32": # Windows...
			print('windows detected')
			pid = os.fork()
			if pid == 0:
				os.setpgrp()
				new = os.fork()
				if new == 0:
					subprocess.call(['python', 'speech.py', text])
					sys.exit(1)
				time.sleep(timeout)
				os.kill(-int(os.getpgrp()), signal.SIGKILL)
				sys.exit(1)
			os.waitpid(pid, 0)

		# time.sleep(5)
		# os.kill(pid, signal.SIGKILL)
		# os.kill(-int(os.getpgrp()), signal.SIGKILL)



		# self.engine.say(text)
		# self.engine.runAndWait()
		print(text)
		pass

