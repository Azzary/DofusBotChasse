import json
import requests

url = "https://github.com/bot4dofus/Datafus/raw/master/data/entities_json/MapPositions.json"
resp = requests.get(url)
data = json.loads(resp.text)

new_data = {}
for elem in data["data"]:
    new_data[elem["id"]] = elem

with open('MapPositions.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)