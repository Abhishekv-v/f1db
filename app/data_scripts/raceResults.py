import requests
import xml.etree.ElementTree as ET
import mysql.connector
import time
import json
# Connecting to Mysql database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1420",
    database="f1db"
)
data_file = "race_results.json"
try:
    with open(data_file, "r") as f:
        results = json.load(f)
        print("Loaded existing data, resuming fetch...")
except FileNotFoundError:
    results = []

resultsURL = "https://ergast.com/api/f1/results"

def time_to_millis(t):
    mins, rest = t.split(":")
    secs, millis = rest.split(".")
    return int(mins)*60000 + int(secs)*1000 + int(millis)

limit = 30
offset = 0
ns = {'ns': 'http://ergast.com/mrd/1.5'}
i = 0
# while True:
#     response = requests.get(f"{resultsURL}?limit={limit}&offset={offset}")
#     root = ET.fromstring(response.content)
#     total = int(root.get('total'))

#     if response.status_code != 200:
#         print(f"Error fetching data: {response.status_code}, Retrying...")
#         time.sleep(10)
#         continue

#     for race in root.findall('ns:RaceTable/ns:Race', ns):
#         season_year = int(race.get("season"))
#         round_ = int(race.get("round"))
#         race_name = race.find('ns:RaceName', ns).text
#         circuit_name = race.find("ns:Circuit", ns).find("ns:CircuitName", ns).text
    
#         results_list = race.find('ns:ResultsList', ns)  
#         if results_list:
#             for result in results_list.findall('ns:Result', ns): 
#                 position = result.get("position")
#                 points = result.get("points")
#                 status = result.find("ns:Status", ns).text

#                 driver = result.find("ns:Driver", ns)
#                 driver_name = driver.find("ns:GivenName", ns).text + " " + driver.find("ns:FamilyName", ns).text
#                 fastest_lap = result.find("ns:FastestLap", ns)
#                 if fastest_lap is not None:
#                     lap_time_elem = fastest_lap.find("ns:Time", ns)
#                     lap_time = lap_time_elem.text if lap_time_elem is not None else None
#                     millis = time_to_millis(lap_time) if lap_time else None
#                 else:
#                     lap_time = None
#                     millis = None
#                 constructor = result.find("ns:Constructor", ns)
#                 constructor_name = constructor.find("ns:Name", ns).text
#                 result_data = {
#                     "season_year": season_year,
#                     "round": round_,
#                     "race_name": race_name,
#                     "circuit_name": circuit_name,
#                     "position": position,
#                     "points":  points,
#                     "status": status, 
#                     "driver_name": driver_name,
#                     "constructor_name": constructor_name,
#                     "Fastest_lap": lap_time,
#                     "millis": millis
#                 }
#                 print(result_data)
#                 results.append(result_data)

#     with open(data_file, "w") as f:
#         json.dump(results, f, indent=4)

#     print(f"Fetched {offset + 30} races so far...")
        
#     if offset + limit >= total:
#         break
#     offset += limit

with open("race_results.json", "r") as f:
    races_data = json.load(f)

cursor = conn.cursor()
cursor = conn.cursor(buffered=True)

for race in races_data:

    season = race["season_year"]
    circuit_name = race["circuit_name"]
    driver_name = race["driver_name"]
    
    constructor_name = race["constructor_name"]
    position = race["position"]
    points = race["points"]
    status = race["status"]
    fastestlap = race["Fastest_lap"]
    millis = race["millis"]
    cursor.execute('SELECT season_id FROM seasons WHERE year = %s', (season,))
    seasonID = cursor.fetchone()[0]

    cursor.execute('SELECT circuit_id FROM circuits WHERE name = %s', (circuit_name,))
    circuitID = cursor.fetchone()[0]

    cursor.execute('SELECT race_id FROM races WHERE season_id = %s AND circuit_id = %s', (seasonID, circuitID))
    raceID = cursor.fetchone()[0]

    cursor.execute('SELECT driver_id FROM drivers WHERE CONCAT(first_name, " ", last_name) like binary %s', (driver_name,))
    #cursor.execute('SELECT driver_id FROM drivers WHERE CONCAT(first_name," ", last_name) = %s', (driver_name,))
    driverID = cursor.fetchone()[0]

    cursor.execute('select constructor_id from constructors WHERE name = %s', (constructor_name,))
    constructorID = cursor.fetchone()[0]

    t_list = [raceID,driverID,constructorID,position,points,status,fastestlap,millis]
    t_tuple = tuple(t_list)
    print(t_tuple)
    cursor.execute('INSERT INTO results (race_id, driver_id, constructor_id, position, points, status,fastestlap_time, fastestlap_milli) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', t_tuple)

print("done")

conn.commit()
conn.close()
