# compare_keys.py

import yaml
import sys
import os

def get_nested(data, key_path):
    keys = key_path.strip().split(".")
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data

with open("old.yml") as f:
    old = yaml.safe_load(f) or {}

with open("new.yml") as f:
    new = yaml.safe_load(f) or {}

watched_keys = yaml.safe_load(os.getenv("WATCHED_KEYS", "{}"))

changed = []

for top_level_key, sub_keys in watched_keys.items():
    for sub_key in sub_keys:
        path = f"{top_level_key}.{sub_key}"
        old_val = get_nested(old, path)
        new_val = get_nested(new, path)
        if old_val != new_val:
            print(f"🔺 Changed: {path} — '{old_val}' → '{new_val}'")
            changed.append(path)

if changed:
    with open(os.environ["GITHUB_OUTPUT"], "a") as out:
        out.write("no_change=false\n")
else:
    print("✅ No watched keys changed.")
    with open(os.environ["GITHUB_OUTPUT"], "a") as out:
        out.write("no_change=true\n")
