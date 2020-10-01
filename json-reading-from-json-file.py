import json
with open('results.json') as json_file:
    data = json.load(json_file)
print(data)