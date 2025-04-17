import requests
import xml.etree.ElementTree as ET
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1420",
    database="f1db"
)

yearURL = "https://ergast.com/api/f1/seasons"

limit = 30
offset = 0
ns = {'ns': 'http://ergast.com/mrd/1.5'}
years = []

while True:
    response = requests.get(f"{yearURL}?limit={limit}&offset={offset}")
    root = ET.fromstring(response.content)
    total = int(root.get('total'))

    for year in root.findall('ns:SeasonTable/ns:Season', ns):
        years.append(year.text)
    # Above loop can also be written as below :)
    #page_years = [season.text for season in root.findall('ns:SeasonTable/ns:Season', ns)]
    #years.extend(page_years)
    if offset + limit >= total:
        break
    offset += limit


cursor = conn.cursor()

for year in years:
   cursor.execute('INSERT INTO seasons (year) VALUES (%s)', (year,))
cursor.execute('SELECT * FROM seasons')
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Year: {row[1]}")
conn.commit()
conn.close()
