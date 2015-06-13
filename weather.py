import json
import urllib2
#herro!
#BIOLER PLATE SHI

def setUrl(city):
	
	
	url = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric'
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = str(opener.open(req).read())
	jsonData = json.loads(f)
	a='temperature='+str(jsonData['main']['temp'])+'\n'
	b='weather='+str(jsonData['weather'][0]['description'])+'\n'
	c='humidity='+str(jsonData['main']['humidity'])
	return a+b+c


	
	
