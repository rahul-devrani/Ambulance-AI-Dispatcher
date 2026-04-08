import json
import os

def load_map(map_name="dehradun_map.json"):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "data", map_name)

    with open(path, "r") as f:
        data = json.load(f)

    return data["nodes"], data["edges"]