import time, os, urllib2, socket, json
from bs4 import BeautifulSoup

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

def what_is(text):
	url = "http://en.wikipedia.org/wiki/"
	url += text.replace(' ','_')

	print("wiki url: "+url)
	try:
		response = urllib2.urlopen(url).read()
	except IOError:
		return 'sorry could not find '+text

	soup = BeautifulSoup(response)

	rem = [soup.findAll('div', {'class':'hatnote'}), soup.findAll('table', {'class','infobox'})]

	for i in rem:
		for x in i:
			x.extract()

	article = soup.findAll('div',{'id':'mw-content-text'})[0]
	description = remove_html_markup(article.p.text)

	return text+description[description.find(' is '):]

def get_local_ip_addr():
	return socket.gethostbyname(socket.getfqdn())

def get_ip_addr():
	response = urllib2.urlopen('http://whatismyip.org').read()
	soup = BeautifulSoup(response)
	x = soup.findAll('span',{'style':'color: blue; font-size: 36px; font-weight: 600;'})
	if len(x) > 0:
		return x[0].text
	else:
		return '127.0.0.1'

def find_city():
	url = "http://api.hostip.info/get_json.php?ip="
	ip = get_ip_addr()
	url += ip
	url += "&position=true"

	print(url)
	try:
		response = urllib2.urlopen(url).read()
	except IOError:
		return 'sorry could not find city from IP: '+ip

	data = json.loads(response)

	if 'city' in data:
		return data['city']
	else:
		return 'no city data found for IP: '+ip

def get_weather(city='blacksburg'):
	url = 'http://api.openweathermap.org/data/2.5/find?q='
	url += city
	url += ',us&units=imperial'

	print(url)
	try:
		response = urllib2.urlopen(url).read()
	except IOError:
		return 'sorry could not find out the weather right now sir.'

	data = json.loads(response)

	temp = int(data['list'][0]['main']['temp'])
	hpa = data['list'][0]['main']['pressure'] # as hPa
	psi = float(hpa * .0145037738)
	hum = data['list'][0]['main']['humidity'] # as percentage
	clouds = data['list'][0]['clouds']['all'] # as percentage
	desc = data['list'][0]['weather'][0]['description']
	w = data['list'][0]['weather'][0]['main']

	s = 'in '+city+', it is currently '
	s += str(temp)+' degrees fahrenheit'
	s += ' with '+desc+'. '
	if hum > 60:
		s += 'It is rather humid today with a humidity of '+str(hum)
		s += ' percent. '

	s += 'Atmospheric pressure is currently '
	s += '%.2f' % psi
	s += ' pounds per square inch. '
	if clouds > 60:
		s += 'also, it is fairly cloudy.'
	return s







