import json
from pathlib import Path

import requests


query = """
[out:json][timeout:45];
way["waterway"="river"]["name"~"Essequibo",i];
out geom;
"""

response = requests.get(
    "https://overpass.kumi.systems/api/interpreter",
    params={"data": query},
    timeout=60,
)
response.raise_for_status()

output = Path(__file__).resolve().parents[1] / "datos" / "essequibo-river.json"
output.write_bytes(response.content)
data = json.loads(response.content)
print([(item["id"], len(item.get("geometry", []))) for item in data.get("elements", [])])
