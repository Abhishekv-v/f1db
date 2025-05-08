import json
from collections import defaultdict
import mysql.connector

# Connecting to Mysql database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1420",
    database="f1db"
)
# with open('sprint_results.json') as f:
#     sprint_data = json.load(f)

# with open('race_results.json') as f:
#     race_data = json.load(f)

# combined = defaultdict(float)

# for entry in sprint_data:
#     key = (entry['season'], entry['round'], entry['driver_name'], entry['constructor_name'])
#     combined[key] += float(entry['points'])

# for entry in race_data:
#     season = str(entry['season_year'])  
#     round_ = str(entry['round'])       
#     key = (season, round_, entry['driver_name'], entry['constructor_name'])
#     combined[key] += float(entry['points'])

# output = [
#     {
#         "season": season,
#         "round": round_,
#         "driver_name": driver_name,
#         "constructor_name": constructor,
#         "total_points": points
#     }
#     for (season, round_, driver_name, constructor), points in combined.items()
# ]

# with open('combined_driver_points.json', 'w') as f:
#     json.dump(output, f, indent=4)


with open('combined_driver_points.json') as f:
    data = json.load(f)

cursor = conn.cursor(buffered=True)

for entry in data:
    season = entry['season']
    driver_name = entry['driver_name']

    cursor.execute('SELECT season_id FROM seasons WHERE year = %s', (season,))
    seasonID = cursor.fetchone()[0]

    cursor.execute('SELECT driver_id FROM drivers WHERE CONCAT(first_name, " ", last_name) like binary %s', (driver_name,))
    driverID = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO driver_standings (season_id, driver_id, points)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE points = VALUES(points)
    """, (
        seasonID,
        driverID,
        entry['total_points']
    ))

conn.commit()
cursor.close()
conn.close()
