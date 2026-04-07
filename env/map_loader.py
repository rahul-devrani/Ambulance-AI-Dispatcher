import json
import os

# Loads Dehradun city graph: 44 nodes (32 locations, 12 hospitals)
# Connectivity weights represent base travel costs for Dijkstra optimization

def load_map(map_name="dehradun_map.json"):
   
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    map_path = os.path.join(base_dir, "data", map_name)
    
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"Map file not found at {map_path}")
        
    with open(map_path, 'r') as f:
        data = json.load(f)
    return data["nodes"], data["edges"]