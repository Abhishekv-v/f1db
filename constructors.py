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

constructorsURL = "https://ergast.com/api/f1/constructors"

limit = 30
offset = 0
ns = {'ns': 'http://ergast.com/mrd/1.5'}
constructors = []

while True:
    response = requests.get(f"{constructorsURL}?limit={limit}&offset={offset}")
    root = ET.fromstring(response.content)
    total = int(root.get('total'))

    for circuit in root.findall('ns:ConstructorTable/ns:Constructor', ns):
        name = circuit.find('ns:Name', ns).text
        nationality = circuit.find('ns:Nationality', ns).text
        constructors.append((name,nationality))

    if offset + limit >= total:
        break
    offset += limit
#print(constructors)
cursor = conn.cursor()

#for constructor in constructors:
#    cursor.execute('INSERT INTO constructors (name, nationality) VALUES (%s,%s)', constructor)
#print('done')
cursor.execute('SELECT * FROM constructors')
rows = cursor.fetchall()
for row in rows:
    print(f"{row[0]},{row[1]},{row[2]} ")
conn.commit()
conn.close()
