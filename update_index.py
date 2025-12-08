#!/usr/bin/env python3
#Auto-generates index.json from mod directories.
#Run: python update_index.py

import json
import os
from datetime import datetime, timezone

def update_index():
    mods_dir = "mods"
    index_path = "index.json"
    
    mod_ids = []
    
    for item in os.listdir(mods_dir):
        item_path = os.path.join(mods_dir, item)
        mod_json_path = os.path.join(item_path, "mod.json")
        
        if os.path.isdir(item_path) and os.path.exists(mod_json_path):
            try:
                with open(mod_json_path, 'r') as f:
                    mod_data = json.load(f)
                
                mod_id = mod_data.get("id")
                if mod_id:
                    expected_dir = mod_id.replace('.', '/')
                    if item == expected_dir.split('/')[-1]:
                        mod_ids.append(mod_id)
                    else:
                        print(f"Warning: Directory '{item}' doesn't match ID '{mod_id}'")
                else:
                    print(f"Missing 'id' field in {mod_json_path}")
                    
            except json.JSONDecodeError:
                print(f"Invalid JSON in {mod_json_path}")
            except Exception as e:
                print(f"Error reading {mod_json_path}: {e}")
    
    mod_ids.sort()
    
    index_data = {
        "schema_version": 1,
        "last_updated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "mods": mod_ids
    }
    
    with open(index_path, 'w') as f:
        json.dump(index_data, f, indent=2)

    print(f"Updated index.json with {len(mod_ids)} mods")
    if mod_ids:
        print("Mods:", ", ".join(mod_ids))
    else:
        print("No mods found")

if __name__ == "__main__":
    update_index()