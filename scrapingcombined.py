# this program web scrapes the url's from Ranger Motor's inventory page
from urllib.request import urlopen
from bs4 import BeautifulSoup

inventory_page = 'http://www.rangermotorsaustin.com/inventory/'

# here we set up the beautiful soup object to extract info from the webpages,
# then pull all the url extensions for each of the cars for sale 
html_inventory = urlopen(inventory_page)
bsObj_inventory = BeautifulSoup(html_inventory.read(), 'html.parser')
url_extensions = bsObj_inventory.findAll('a', {'class':'inv-view-details'})

# here we append all of the car-specific url to the base domain url, 
# so we can go to each car's individual page to get information about it
urls_to_scrape = []
for i in range(len(url_extensions)) :
    current = url_extensions[i]
    url_extension = current.attrs['href']
    print(url_extension)
    extended_url = 'http://www.rangermotorsaustin.com' + url_extension
    urls_to_scrape.append(extended_url)

# now print out the attributes of each car in turn
for i in range(len(urls_to_scrape)):
    car_url = urls_to_scrape[i]
    print (car_url)
    html = urlopen(str(car_url))
    bsObj = BeautifulSoup(html.read(), 'html.parser')
    attribute = bsObj.findAll('span', {'class':'strong'})
    value = bsObj.findAll('span', {'class':'pull-right'})
    aaa_list = bsObj.findAll('li', {'class':'list-group-item'})

    for x in attribute :
        print(x.get_text())
    for y in value :
        print(y.get_text())
