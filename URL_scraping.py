# swagger
# this program web scrapes the url's from Ranger Motor's inventory page
from urllib.request import urlopen
from bs4 import BeautifulSoup


inventory = urlopen('http://www.rangermotorsaustin.com/inventory/')
bsObj_inventory = BeautifulSoup(inventory.read(), 'html.parser')
listing_urls = bsObj_inventory.findAll('a', {'class':'inv-view-details'})


for x in listing_urls :
	print(x.attrs['href'])
