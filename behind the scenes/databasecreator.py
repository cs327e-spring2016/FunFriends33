import pymysql
conn = pymysql.connect(host='localhost', port = 3306,
                        user = 'root', passwd='lenneth6')
    
cur = conn.cursor()
cur.execute("create database rngmotor")
cur.execute("Use rngmotor")

cur.execute("CREATE TABLE inventory " +
            "(vin_number VARCHAR(17)," +
            "make VARCHAR(30)," +
            "model_name VARCHAR(30)," +
            "year SMALLINT UNSIGNED," +
            "mileage INT UNSIGNED," +
            "engine VARCHAR(15)," +
            "transmission ENUM('A','F')," +
            "num_doors SMALLINT UNSIGNED," +
            "conditions VARCHAR(140),"
            "city_fuel_economy SMALLINT UNSIGNED," +
            "hwy_fuel_economy SMALLINT UNSIGNED," +
            "price INT UNSIGNED," +
            "ext_color VARCHAR(20)," +
            "int_color VARCHAR(20)," +
            "date_added date," +
            "CONSTRAINT vn PRIMARY KEY (vin_number)" +
            ");")

cur.close()
conn.close()
