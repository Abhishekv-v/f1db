import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1420",
    database="f1db"
)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        race_id INT NOT NULL,
        driver_id INT NOT NULL,
        constructor_id INT NOT NULL,
        position INT,
        points FLOAT,
        status VARCHAR(255),
        FOREIGN KEY (race_id) REFERENCES races(race_id),
        FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
        FOREIGN KEY (constructor_id) REFERENCES constructors(constructor_id)
    );
''')
conn.commit()
cursor.close()
conn.close()