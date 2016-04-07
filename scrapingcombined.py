# swagger
# this program web scrapes the url's from Ranger Motor's inventory page
from urllib.request import urlopen
from bs4 import BeautifulSoup


inventory = urlopen('http://www.rangermotorsaustin.com/inventory/')
bsObj_inventory = BeautifulSoup(inventory.read(), 'html.parser')
listing_urls = bsObj_inventory.findAll('a', {'class':'inv-view-details'})

url=[]
i = 0
for x in listing_urls :
	print(x.attrs['href'])
	
	url.append("http://www.rangermotorsaustin.com")
	url[i] += x.attrs['href']
	i+=1
print (url[0])

html = urlopen(str(url[0]))
bsObj = BeautifulSoup(html.read(), 'html.parser')
attribute = bsObj.findAll('span', {'class':'strong'})
value = bsObj.findAll('span', {'class':'pull-right'})
aaa_list = bsObj.findAll('li', {'class':'list-group-item'})


for x in attribute :
	print(x.get_text())
for y in value :
	print(y.get_text())
