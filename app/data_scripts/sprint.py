import requests
import xml.etree.ElementTree as ET
import json

limit = 30
offset = 0
ns = {'ns': 'http://ergast.com/mrd/1.5'}
url = "https://ergast.com/api/f1/sprint"
sprint_results = []

while True:
    response = requests.get(f"{url}?limit={limit}&offset={offset}")
    root = ET.fromstring(response.content)
    total = int(root.get('total'))

    for race in root.findall('ns:RaceTable/ns:Race', ns):
        season = race.get('season')
        round_ = race.get('round')

        for sprint in race.findall('.//ns:SprintResult', ns):
            points = sprint.get('points')
            given_name = sprint.find('ns:Driver/ns:GivenName', ns).text
            family_name = sprint.find('ns:Driver/ns:FamilyName', ns).text
            driver_name = f"{given_name} {family_name}"

            constructor_name = sprint.find('ns:Constructor/ns:Name', ns).text

            sprint_results.append({
                "season": season,
                "round": round_,
                "driver_name": driver_name,
                "constructor_name": constructor_name,
                "points": points
            })

    if offset + limit >= total:
        break
    offset += limit

with open('app/data_scripts/sprint_results.json', 'w') as json_file:
    json.dump(sprint_results, json_file, indent=4)

print("Saved sprint_results.json.")
