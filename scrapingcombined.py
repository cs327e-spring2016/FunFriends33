from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

<<<<<<< Updated upstream
def scrape ():

    # this program web scrapes the url's from Ranger Motor's inventory page

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
        extended_url = 'http://www.rangermotorsaustin.com' + url_extension
        urls_to_scrape.append(extended_url)

    # now print out the attributes of each car in turn
    for i in range(len(urls_to_scrape)):
        car_url = urls_to_scrape[i]
        html = urlopen(str(car_url))
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        attribute = bsObj.findAll('span', {'class':'strong'})
        value = bsObj.findAll('span', {'class':'pull-right'})
        aaa_list = bsObj.findAll('li', {'class':'list-group-item'})



        value2 = []
        attribute2 = []
        for y in value :
            value2.append(y.get_text())
        for z in attribute :
            attribute2.append(z.get_text())


        dbwrite(value2, attribute2)

#values and attributes are pairwise the same length
#but they are not the same length all the time, so we need to check the attributes that a given car has before entering.
#If a value is not there we need to add null instead
#fill the values with null.

def dbwrite (values, attributes):

    conn = pymysql.connect(host='localhost', port = 3306,
                        user = 'root', passwd='lenneth6')

    cur = conn.cursor()

    cur.execute("use rngmotors")

    cur.execute("SELECT vin_number from inventory")


    #this checks that the vin number is not already in the table
    vinlist = list(cur.fetchall())
    for i in range(len(vinlist)) :
        if vinlist[i] == attributes[12] :
            return

    print(len(attributes))
    print (attributes)
    #attribute[12] is the vin number
    stringer = str("INSERT INTO inventory (vin_number, model_name, ext_color_id, int_color_id) VALUES (" + attributes[12] +"," + attributes[2] + "," +  attributes[9] + "," + attributes[10] + ")")
    stringer2 = str("UPDATE inventory set year =" + attributes[0] + ", mileage =" + attributes[4] + ", conditions = " + attributes[14] + "WHERE vin_number = " + attributes[12])

    print (stringer)
    print (stringer2)

    #id 13 to not be in the database

    cur.close()

    conn.close()


def main():
    #ask the user what they want to do
    #if data queary
    #if update table scrape
    #if update validation
    scrape()


main()
=======
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

>>>>>>> Stashed changes
