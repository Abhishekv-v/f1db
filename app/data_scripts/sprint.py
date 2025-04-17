import requests
import xml.etree.ElementTree as ET
import json

limit = 30
offset = 0
ns = {'ns': 'http://ergast.com/mrd/1.5'}
years = []
url = "https://ergast.com/api/f1/sprint"
while True:
    response = requests.get(f"{url}?limit={limit}&offset={offset}")
    root = ET.fromstring(response.content)
    total = int(root.get('total'))

    for race in root.findall('ns:RaceTable/ns:Race', ns):
        

        races.append((seasonID, circuitID, roundNo, raceName, raceDate))
    if offset + limit >= total:
        break
    offset += limit
# Save the extracted data to a JSON file
def save_to_json(data):
    with open('sprint_results.json', 'w') as f:
        json.dump(data, f, indent=4)

# Main function to fetch, extract, and save the data
def main():
    # Fetch data from Ergast API
    root = fetch_data()
    
    if root is not None:
        # Extract relevant data
        sprint_results = extract_relevant_data(root)
        
        # Save the data to a JSON file
        save_to_json(sprint_results)
        print("Data has been saved to sprint_results.json")

# Run the main function
if __name__ == "__main__":
    main()
