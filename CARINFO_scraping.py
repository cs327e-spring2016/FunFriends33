# more swagger
# this program web scrapes the information from a car's listing page

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.rangermotorsaustin.com/inventory/view/8905508/2007-Chevrolet-Silverado-2500HD-Classic-2WD-Crew-Cab-153%22-Work-Truck-Austin-TX")
bsObj = BeautifulSoup(html.read(), 'html.parser')
attribute = bsObj.findAll('span', {'class':'strong'})
value = bsObj.findAll('span', {'class':'pull-right'})
aaa_list = bsObj.findAll('li', {'class':'list-group-item'})


for x in attribute :
	print(x.get_text())
for y in value :
	print(y.get_text())