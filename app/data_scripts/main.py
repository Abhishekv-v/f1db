import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1420",
    database="f1db"
)
cursor = conn.cursor()
#cursor.execute('CREATE DATABASE IF NOT EXISTS f1db')

# Seasons Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS seasons (
        season_id INT AUTO_INCREMENT PRIMARY KEY,
        year INT NOT NULL UNIQUE
    );
''')

# Circuits Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS circuits (
        circuit_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        locality VARCHAR(255),
        country VARCHAR(255),
        latitude DECIMAL(10, 7),
        longitude DECIMAL(10, 7)
    );
''')

# Race Schedule Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS races (
        race_id INT AUTO_INCREMENT PRIMARY KEY,
        season_id INT NOT NULL,
        circuit_id INT NOT NULL,
        round INT,
        name VARCHAR(255) NOT NULL,
        raceDate DATE,
        FOREIGN KEY (season_id) REFERENCES seasons(season_id),
        FOREIGN KEY (circuit_id) REFERENCES circuits(circuit_id)
    );
''')

# Drivers Data Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS drivers (
        driver_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        dob DATE,
        nationality VARCHAR(255),
        birthdate DATE
    );
''')

# Constructors Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS constructors (
        constructor_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        nationality VARCHAR(255)
    );
''')

# Race Results Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        race_id INT NOT NULL,
        driver_id INT NOT NULL,
        constructor_id INT NOT NULL,
        position INT,
        points FLOAT,
        status VARCHAR(255),
        fastestlap_time VARCHAR(10),
        fastestlap_milli INT,
        FOREIGN KEY (race_id) REFERENCES races(race_id),
        FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
        FOREIGN KEY (constructor_id) REFERENCES constructors(constructor_id)
    );
''')

# Qualifying Results Table
# Note: Qualifying results are only fully supported from the 2003 season onwards.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS qualifying (
        qualifying_id INT AUTO_INCREMENT PRIMARY KEY,
        race_id INT NOT NULL,
        driver_id INT NOT NULL,
        position INT,
        q1_time TIME,
        q2_time TIME,
        q3_time TIME,
        FOREIGN KEY (race_id) REFERENCES races(race_id),
        FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
    );
''')

# Drivers Standing Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS driver_standings (
        standing_id INT AUTO_INCREMENT PRIMARY KEY,
        season_id INT NOT NULL,
        driver_id INT NOT NULL,
        points FLOAT,
        FOREIGN KEY (season_id) REFERENCES seasons(season_id),
        FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
    );
''')

# Constructors Standing Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS constructor_standings (
        standing_id INT AUTO_INCREMENT PRIMARY KEY,
        season_id INT NOT NULL,
        constructor_id INT NOT NULL,
        points FLOAT,
        FOREIGN KEY (season_id) REFERENCES seasons(season_id),
        FOREIGN KEY (constructor_id) REFERENCES constructors(constructor_id)
    );
''')

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

