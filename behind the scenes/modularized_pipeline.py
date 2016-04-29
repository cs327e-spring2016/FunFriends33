# SCRAPE DATA FROM RANGERMOTORSAUSTIN AND WRITE IT TO OUR DATABASE!

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

# scrape all listing urls and returns a list of listing urls
def get_list_of_listing_urls () : 
	
	inventory = urlopen('http://www.rangermotorsaustin.com/inventory/')
	soup_inventory = BeautifulSoup(inventory.read(), 'html.parser')

	listing_tags = soup_inventory.findAll('a', {'class':'inv-view-details'})
	listing_urls = []

	for tag in listing_tags :
		url = 'http://www.rangermotorsaustin.com' + tag.attrs['href']
		listing_urls.append(url)

	return listing_urls	

# return dictionaries full of relevant data given a list of urls
def get_list_of_dictionaries (urls) : 

	list_of_listing_dictionaries = []

	for url in urls :
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
		listing_dictionary['Price'] = price
		print('SCRAPED ' + listing_dictionary['Make'] + ' : ' + listing_dictionary['Model'])

		list_of_listing_dictionaries.append(listing_dictionary)

	return list_of_listing_dictionaries

# fill in nulls for each dictionary and returns the modified list of dictionaries
def fill_in_nulls (list_of_dictionaries) : 

	list_of_keys = ['Price', 'Year', 'Make', 'Model', 'Body style', 'Mileage', 'Transmission', 'Engine', 'Drivetrain', 'Exterior', 'Interior', 'Doors', 'Stock', 'VIN', 'Fuel Mileage', 'Conditon']

	for l in list_of_dictionaries :
		for k in list_of_keys :
			if not (k in l) :
				l[k] = 'NULL'

	return list_of_dictionaries

# change data types from string to integers where applicable and returns the modified list of dictionaries
def fix_data_types(list_of_dictionaries) : 
	
	for l in list_of_dictionaries :
		if not (l['Doors'] == 'NULL') :
			l['Doors'] = l['Doors'][0]
		l['Mileage'] = l['Mileage'].replace(',', '')

	return list_of_dictionaries

# create insert statement for each car and returns a list of insert statements
def create_list_of_insert_statements (list_of_dictionaries, vins) : 
	list_of_insert_statements = []
	for l in list_of_dictionaries :
		b = False
		for v in vins :
			if l['VIN'] == v[0] :
				b = True
		if not b :
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

	return list_of_insert_statements

urls = get_list_of_listing_urls()

dictionaries = get_list_of_dictionaries(urls)
dictionaries = fill_in_nulls(dictionaries)
dictionaries = fix_data_types(dictionaries)

# connect to database and write data into
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='MyNewPass', db='mysql')
cur = conn.cursor()

# THIS IS WHERE YOU CHANGE THE DATABASE USED
cur.execute('USE FunFriends33')

# get all vins to check against
cur.execute('select vin from CarsForSale')
vins = cur.fetchall()

insert_statements = create_list_of_insert_statements(dictionaries, vins)

print('WRITE DATA INTO DATABASE')
for ins_st in insert_statements :
	cur.execute(ins_st)

cur.close()
conn.commit()
conn.close()




# end of file