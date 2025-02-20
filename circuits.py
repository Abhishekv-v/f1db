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

circuitsURL = "https://ergast.com/api/f1/circuits"

limit = 30
offset = 0
ns = {'ns': 'http://ergast.com/mrd/1.5'}
circuits = []

while True:
    response = requests.get(f"{circuitsURL}?limit={limit}&offset={offset}")
    root = ET.fromstring(response.content)
    total = int(root.get('total'))

    for circuit in root.findall('ns:CircuitTable/ns:Circuit', ns):
        circuit_name = circuit.find('ns:CircuitName', ns).text
        locality = circuit.find('ns:Location/ns:Locality', ns).text
        country = circuit.find('ns:Location/ns:Country', ns).text
        circuits.append((circuit_name,locality,country))

    if offset + limit >= total:
        break
    offset += limit

cursor = conn.cursor()

for circuit in circuits:
    cursor.execute('INSERT INTO circuits (name, locality, country) VALUES (%s,%s,%s)', circuit)

cursor.execute('SELECT * FROM circuits')
rows = cursor.fetchall()
for row in rows:
    print(f"{row[0]},{row[1]},{row[3]} ")
conn.commit()
conn.close()
