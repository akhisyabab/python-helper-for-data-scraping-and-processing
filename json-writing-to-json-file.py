import json
data = {
    'name': 'Akhi',
    'age': '23',
    'country': 'Indonesia'
}
with open('results.json', 'w') as outfile:
    json.dump(data, outfile)