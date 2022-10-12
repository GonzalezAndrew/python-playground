import json

data = [{"name": "test"}]

data = json.dumps(data)

with open("data.json", "w") as out:
    json.dump(data, out, indent=4)
