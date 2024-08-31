import json

with open('image_map.json', 'r', encoding='utf8') as mapfile:
    raw_mappings = json.load(mapfile)

mappings = {}

for i in raw_mappings:
    mappings[i['name']] = i['file_name']

def get_filename(name: str) -> str | None:
    if name in mappings:
        return mappings[name]
    return None

def get_all_names() -> list:
    return mappings.keys()

def get_all_files() -> list:
    return mappings.values()