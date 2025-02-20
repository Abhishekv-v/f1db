import requests
import xml.etree.ElementTree as ET
import mysql.connector

# Connecting to Mysql database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1420",
    database="f1db"
)

driversURL = "https://ergast.com/api/f1/drivers"

limit = 30
offset = 0
ns = {'ns': 'http://ergast.com/mrd/1.5'}
drivers = []

while True:
    response = requests.get(f"{driversURL}?limit={limit}&offset={offset}")
    root = ET.fromstring(response.content)
    total = int(root.get('total'))
    for driver in root.findall('ns:DriverTable/ns:Driver', ns):
        firstname = driver.find('ns:GivenName', ns).text
        lastname = driver.find('ns:FamilyName', ns).text
        nationality = driver.find('ns:Nationality', ns).text
        birthdate = driver.find('ns:DateOfBirth', ns).text
        drivers.append((firstname,lastname,nationality,birthdate))

    if offset + limit >= total:
        break
    offset += limit
cursor = conn.cursor()

#for driver in drivers:
#    cursor.execute('INSERT INTO drivers (first_name,last_name,nationality,birthdate) VALUES (%s,%s,%s,%s)', driver)
#print("done")
cursor.execute('SELECT * FROM drivers')
rows = cursor.fetchall()
for row in rows:
    print(f"{row[0]},{row[1]},{row[3]} ")
conn.commit()
conn.close()
