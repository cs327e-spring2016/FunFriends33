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
            "CONSTRAINT vn PRIMARY KEY (vin_number), " +
            "CONSTRAINT mdl FOREIGN KEY (model_name) " +
            "REFERENCES models (model_name)" +
            ");")

cur.execute("ALTER TABLE inventory " +
            "ADD year SMALLINT UNSIGNED," +
            "ADD mileage INT UNSIGNED," +
            "ADD transmission ENUM('A','F')," +
            "ADD num_doors SMALLINT UNSIGNED," +
            "ADD conditions VARCHAR(140)" )

cur.execute("Alter Table inventory " +
            "ADD city_fuel_economy SMALLINT UNSIGNED," +
            "ADD hwy_fuel_economy SMALLINT UNSIGNED," +
            "ADD price INT UNSIGNED," +
            "ADD price_notes VARCHAR(140)")

cur.execute("ALTER TABLE inventory " +
            "ADD ext_color_id SMALLINT UNSIGNED")

cur.execute("ALTER TABLE inventory " +
            "ADD CONSTRAINT colorext FOREIGN KEY (ext_color_id) " +
            "REFERENCES colors (color_id)" )

cur.execute("ALTER TABLE inventory " +
            "ADD int_color_id SMALLINT UNSIGNED," +
            "ADD CONSTRAINT colorint FOREIGN KEY (int_color_id) " +
            "REFERENCES colors (color_id)")
            
cur.close()
conn.close()
