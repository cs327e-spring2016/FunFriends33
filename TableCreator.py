import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='MyNewPass', db='mysql')

cur = conn.cursor()
#		THIS IS WHERE YOU CHANGE THE DATABASE USED
cur.execute('USE FunFriends33')
cur.execute('''CREATE TABLE CarsForSale (
	VIN varchar(30) primary key,
	Price int,
	Year year,
	Make varchar(30),
	Model varchar(30),
	Body_Style varchar(30),
	Mileage int,
	Transmission varchar(30),
	Engine varchar(30),
	Drivetrain varchar(30),
	Exterior varchar(30),
	Interior varchar(30),
	Doors int,
	Stock varchar(30),
	Fuel_Mileage varchar(30),
	Conditon varchar(30))''')
cur.close()

conn.commit()
conn.close()