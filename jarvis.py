import jio, time, os, webbrowser, sys, signal, jarvis_util
from sys import platform as _platform

config = {}
execfile("config.py", config)

io = jio.JarvisIO()

def main():
	# io.listen_for('Jarvis')
	io.say('hello sir, what do you need?')
	# print('Yes, sir?')
	while True:
		try:
			command(io.next())
		except IOError:
			print("hmmm, something weird happened...")
		time.sleep(0.1)
	pass

def command(text):
	if len(text) == 0:
		return
	args = text.split()
	if 'hello' in args and len(args) < 4:
		io.say('hello, sir')
	elif 'jarvis' in args and 'terminate' in args and len(args) < 5:
		io.say('farewell sir')
		sys.exit(1)
	elif 'jarvis' in args and 'lock' in args and len(args) < 3:
		io.say('I will stop listening now sir')
		while True:
			try:
				text = io.next()
				args = text.split()
				if 'jarvis' in args and 'unlock' in args and len(args) < 4:
					io.say('I am listening again sir')
					break
			except IOError:
				print('oops, something weird happened')
			time.sleep(0.1)
	elif 'where' in args:
		if 'am' in args and 'i' in args:
			io.say(jarvis_util.find_city())
		pass
	elif 'weather' in args:

		io.say(jarvis_util.get_weather(city='centreville'), 20)
		# url = 'http://www.google.com/search?q=weather'
		# webbrowser.open(url)
		pass
	elif 'what is' in text or 'who is' in text:
		text = text.replace('what is ','')
		text = text.replace('who is ','')
		text = text.replace('jarvis', '')
		text = text.replace('a ', '') # this may cause problems
		desc = jarvis_util.what_is(text)
		for i in range(10):
			desc = desc.replace('['+str(i)+']', '')
		io.say(desc, 30)
		pass
	elif 'search' in args[:4]:
		rem = ['search', 'jarvis', 'for']
		for x in rem:
			try:
				args.remove(x)
			except ValueError:
				pass

		keyword = ' '.join(args)
		io.say('Beginning a google search for: '+keyword)
		url = 'http://www.google.com/search?q='+keyword
		webbrowser.open(url)
	elif 'open' in args or 'start' in args or 'launch' in args:
		rem = ['open', 'start', 'launch', 'jarvis']
		for x in rem:
			try:
				args.remove(x)
			except ValueError:
				pass

		appname = ' '.join(args)
		args.insert(0, appname)

		# remove clutter words
		for arg in args:
			if arg in config['stop_words']:
				args.remove(arg)

		# search for app in /Applications
		for arg in args:
			for app in config['apps']:
				if arg in app.lower():
					print(arg + " was found in " + app.lower())
					if _platform == "linux" or _platform == "linux2": # linux
					    pass
					elif _platform == "darwin": # OS X
					    os.system('/usr/bin/open -a "/Applications/'+app+'"')
					    io.say('opening '+app[:len(app)-4])
					    pass
					elif _platform == "win32": # Windows...
					    pass
					return


		# if nothing left, then stop
		if len(args) < 0:
			return

		# check web apps
		keyword = args[0]
		if keyword in config['webapps']:
			io.say('opening '+keyword+' for you, sir.')
			url = 'http://www.google.com/search?q='+keyword+'&btnI'
			webbrowser.open(url)
	elif 'close' in args or 'exit' in args:
		rem = ['close', 'exit', 'jarvis']
		for x in rem:
			try:
				args.remove(x)
			except ValueError:
				pass

		for arg in args:
			for app in config['app_names']:
				if arg in app.lower():
					print(arg + " was found in " + app.lower())
					os.system('killall "'+app+'"')
					io.say('closing '+app)

		pass
	else:
		print("not a command")
	pass

if __name__ == '__main__':
	main()