import os

stop_words = open('stop-word-list.txt').read().lower().split()

apps = os.listdir('/Applications')

app_names = []

removed = []
for app in apps:
	if '.app' not in app:
		apps.remove(app)
		removed.append(app)
apps.remove('Utilities')

app_names += apps

removed.append('Utilities')
for a in removed:
	try:
		more = os.listdir('/Applications/'+str(a))
		apps += [(str(a)+'/'+x) for x in more if '.app' in x and 'uninstall' not in x]
		app_names += [x for x in more if '.app' in x and 'uninstall' not in x]
	except OSError:
		continue
apps.sort()

for name in app_names:
	if '.app' not in name:
		app_names.remove(name)

for x in range(len(app_names)):
	app_names[x] = app_names[x][:len(app_names[x])-4]

print(app_names)

webapps = ['netflix', 'facebook', 'twitter', 'youtube']