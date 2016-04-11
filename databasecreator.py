import pymysql
conn = pymysql.connect(host='localhost', port = 3306,
                        user = 'root', passwd='lenneth6')

cur = conn.cursor()
cur.execute("create database rngmotors")
cur.execute("Use rngmotors")
cur.execute("CREATE TABLE models" +
            "(model_name VARCHAR(30)," +
            "make VARCHAR(30)," +
            "CONSTRAINT modelname PRIMARY KEY (model_name)" +
            ");")
cur.execute("CREATE TABLE colors" +
            "(color_id SMALLINT UNSIGNED," +
            "color_name VARCHAR(25)," +
            "CONSTRAINT colorid PRIMARY KEY (color_id)" +
            ");")

cur.execute("CREATE TABLE inventory" +
            "(vin_number VARCHAR(16)," +
            "model_name VARCHAR(20)," +
            "year SMALLINT UNSIGNED," +
            "mileage INT UNSIGNED," +
            "transmission ENUM('A','F')," +
            "num_doors SMALLINT UNSIGNED," +
            "condition VARCHAR(140)," +
            "city_fuel_economy SMALLINT UNSIGNED," +
            "hwy_fuel_economy SMALLINT UNSIGNED," +
            "price INT UNSIGNED," +
            "price_notes VARCHAR(140)," +
            "ext_color_id SMALLINT UNSIGNED," +
            "int_color_id SMALLINT UNSIGNED," +
            "CONSTRAINT vn PRIMARY KEY (vin_number)" +
            "CONSTRAINT model FOREIGN KEY (model_name)" +
            "REFERENCES models (modelname)" +
            "CONSTRAINT color FOREIGN KEY (ext_color_id)" +
            "REFERENCES colors (color_id)" +
            "CONSTRAINT color FOREIGN KEY (int_color_id" +
            "REFERENCES colors (color_id)" +
            ");")
            
cur.close()
conn.close()







#conn  = pymysql.connect(host='localhost', port = 3306,
#                        user = 'root', passwd='lenneth6', db = 'bank')


#cur = conn.cursor()

#cur.execute("Use bank")
#cur.execute("Select * FROM person WHERE person_id=1")
#print(cur.fetchone())
#cur.close()
#conn.close()
