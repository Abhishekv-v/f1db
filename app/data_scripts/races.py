import requests
import xml.etree.ElementTree as ET
import mysql.connector
import time

# Connecting to Mysql database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1420",
    database="f1db"
)

racesURL = "https://ergast.com/api/f1/races"

limit = 30
offset = 0
ns = {'ns': 'http://ergast.com/mrd/1.5'}
races = []
while True:
    response = requests.get(f"{racesURL}?limit={limit}&offset={offset}")
    root = ET.fromstring(response.content)
    total = int(root.get('total'))

    for race in root.findall('ns:RaceTable/ns:Race', ns):
        raceName = race.find('ns:RaceName', ns).text
        season = race.get("season")
        roundNo = race.get("round")
        circuit = race.find("ns:Circuit", ns)
        circuit_id = circuit.get("circuitId")
        circuit_name = circuit.find("ns:CircuitName", ns).text
        raceDate = race.find('ns:Date', ns).text
        cursor = conn.cursor()
        cursor.execute('SELECT season_id FROM seasons WHERE year = %s', (season,))
        seasonID = cursor.fetchone()[0]

        cursor.execute('SELECT circuit_id FROM circuits WHERE name = %s', (circuit_name,))
        circuitID = cursor.fetchone()[0]

        races.append((seasonID, circuitID, roundNo, raceName, raceDate))
    if offset + limit >= total:
        break
    offset += limit

cursor = conn.cursor()

for race in races:
   cursor.execute('INSERT INTO races (season_id, circuit_id, round, name, raceDate) VALUES (%s,%s,%s,%s,%s)', race)
print('done')
# cursor.execute('SELECT * FROM races')
# rows = cursor.fetchall()
# for row in rows:
#     print(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}")
conn.commit()
conn.close()
