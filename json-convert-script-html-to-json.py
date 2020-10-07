import json
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('res.html'), 'html.parser')

scripts = soup.find_all('script')
selected_script = None
for script in scripts:
    if 'window.__APOLLO_STATE__=' in str(script):
        selected_script = script

selected_script = selected_script.text
selected_script = selected_script.replace('window.__APOLLO_STATE__=', '').replace(';', '')
converted_script = json.loads(selected_script)

with open('converted_script.json', 'w') as outfile:
    json.dump(converted_script, outfile)