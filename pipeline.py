##### SOME CLEAN STUFF ;) 

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

# scrape all listing urls

inventory = urlopen('http://www.rangermotorsaustin.com/inventory/')
soup_inventory = BeautifulSoup(inventory.read(), 'html.parser')

listing_tags = soup_inventory.findAll('a', {'class':'inv-view-details'})
listing_urls = []

for tag in listing_tags :
	url = 'http://www.rangermotorsaustin.com' + tag.attrs['href']
	listing_urls.append(url)

list_of_listing_dictionaries = []

# now for each individual listing : scrape all available key/value pairs into a dictionary and append the dictionary to our list of listing dictionaries
# IMPORTANT --------- STILL NEED TO SCRAPE THE PRICE
for url in listing_urls :
	u = urlopen(url)
	soup_listing = BeautifulSoup(u.read(), 'html.parser')

	listing_dictionary = {}
	ul_listgroup_tag = soup_listing.find('ul', class_='list-group')
	li_listgroupitem_tags = ul_listgroup_tag.find_all('li', class_='list-group-item')
	li_listgroupitem_tags = li_listgroupitem_tags[:-1]

	for tag in li_listgroupitem_tags :
		span_tags = tag.find_all('span')
		key = span_tags[0].get_text().strip()
		val = span_tags[1].get_text().strip()
		listing_dictionary[key] = val

	price = soup_listing.find('span', {'class':'details-price'}).get_text()
	price = price.split()[2]
	price = price.strip().replace(',', '').replace('$', '')
	print(price)
	listing_dictionary['Price'] = price

	list_of_listing_dictionaries.append(listing_dictionary)

list_of_keys = ['Price', 'Year', 'Make', 'Model', 'Body style', 'Mileage', 'Transmission', 'Engine', 'Drivetrain', 'Exterior', 'Interior', 'Doors', 'Stock', 'VIN', 'Fuel Mileage', 'Conditon']

# fill in nulls
for l in list_of_listing_dictionaries :
	for k in list_of_keys :
		if not (k in l) :
			l[k] = 'NULL'

# fix data types
for l in list_of_listing_dictionaries :
	if not (l['Doors'] == 'NULL') :
		l['Doors'] = l['Doors'][0]
	l['Mileage'] = l['Mileage'].replace(',', '')


# create insert statement for each car

list_of_insert_statements = []
for l in list_of_listing_dictionaries :
#		THIS IS WHERE YOU CHANGE THE TABLE INTO WHICH YOU INSERT RECORDS
	insert_statement = 'INSERT INTO CarsForSale SET '
	for key in l :
		if key == 'Body style' :
			insert_statement = insert_statement + 'Body_Style=("' + l[key] + '"), '
		elif key == 'Fuel Mileage' :
			insert_statement = insert_statement + 'Fuel_Mileage=("' + l[key] + '"), '
		else :
			if not (l[key] == 'NULL') :
				insert_statement = insert_statement + key + '=("' + l[key] + '"), '	
	insert_statement = insert_statement[:-2]
	list_of_insert_statements.append(insert_statement)

# maybe we should check the table for what vin numbers are already entries and update those?
# but as long as we're creating the db/table at run time that really shouldn't be a concern

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='MyNewPass', db='mysql')

cur = conn.cursor()
#		THIS IS WHERE YOU CHANGE THE DATABASE USED
cur.execute('USE FunFriends33')
for ins_st in list_of_insert_statements :
	cur.execute(ins_st)
cur.close()

conn.commit()
conn.close()




# end of file