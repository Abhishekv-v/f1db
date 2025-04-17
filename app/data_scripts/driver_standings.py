import json
from collections import defaultdict

# Load your JSON data
with open('app/data_scripts/race_results.json') as f:
    race_data = json.load(f)

# Store cumulative points: { (season, driver): total_points }
cumulative_points = defaultdict(float)

# To store final output
driver_standings = []

# Sort the data by season and round
race_data.sort(key=lambda x: (x['season_year'], x['round']))

# Loop through race results
for result in race_data:
    season = result['season_year']
    round_ = result['round']
    driver = result['driver_name']
    points = float(result['points']) if result['points'] else 0.0

    # Add to cumulative total
    cumulative_points[(season, driver)] += points

    # Store this snapshot of standings
    driver_standings.append({
        "season": season,
        "round": round_,
        "driver_name": driver,
        "points": cumulative_points[(season, driver)]
    })

# Optional: group standings by round to see top drivers after each race
from pprint import pprint
pprint(driver_standings)

