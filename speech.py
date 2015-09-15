import sys, pyttsx

def main():
	if len(sys.argv) < 2:
		return
	text = sys.argv[1]
	engine = pyttsx.init()
	engine.say(text)
	engine.runAndWait()

if __name__ == '__main__':
	main()